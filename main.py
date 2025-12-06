import traceback
from datetime import datetime
import time
from collections import deque  # Added for buffering

from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from UI import Ui_MainWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog

import cv2
import os
import numpy as np
import csv
import winsound  # Added for voice warning
import threading

from ultralytics import YOLO
from tool.parser import get_config
from tool.tools import draw_info, result_info_format, format_data, writexls, writecsv, resize_with_padding


class CSVReaderThread(QThread):
    data_signal = pyqtSignal(dict)
    danger_signal = pyqtSignal(bool)

    def __init__(self, csv_path):
        super().__init__()
        self.csv_path = csv_path
        self.running = True
        self.last_pos = 0
        self.buffer = deque()

    def _reader_loop(self):
        """Producer: Reads file and fills buffer continuously"""
        # Initial seek
        if os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, 'r', encoding='utf-8') as f:
                    f.seek(0, 2)
                    self.last_pos = f.tell()
            except:
                pass

        while self.running:
            try:
                if os.path.exists(self.csv_path):
                    with open(self.csv_path, 'r', encoding='utf-8') as f:
                        f.seek(0, 2)
                        current_end = f.tell()
                        if self.last_pos > current_end:
                            self.last_pos = 0

                        f.seek(self.last_pos)
                        lines = f.readlines()
                        self.last_pos = f.tell()

                        if lines:
                            for line in lines:
                                if line.strip():
                                    self.buffer.append(line.strip())
            except Exception:
                pass

            # Sleep to allow file updates
            time.sleep(0.05)

    def run(self):
        """Consumer: Emits data from buffer with elastic pacing"""
        # Start reader in background thread
        threading.Thread(target=self._reader_loop, daemon=True).start()

        while self.running:
            if not self.buffer:
                # Buffer empty, wait a bit
                time.sleep(0.005)
                continue

            # Pop and emit
            try:
                line = self.buffer.popleft()
                self.process_and_emit(line)
            except IndexError:
                continue

            # Elastic Pacing
            buffer_size = len(self.buffer)

            if buffer_size > 100:
                time.sleep(0.002)  # Catch up fast
            elif buffer_size > 50:
                time.sleep(0.01)
            elif buffer_size > 10:
                time.sleep(0.03)  # Normal speed ~30fps
            else:
                # Low buffer, slow down to stretch data until next read fills it
                time.sleep(0.08)

    def process_and_emit(self, line):
        try:
            parts = line.split(',')
            # Columns: 0:Time, 1:Device, 2:DispX, 3:DispY, 4:VelX, 5:VelY, 6:AngX, 7:AngY, 8:AngZ
            vel_x = float(parts[4]) if len(parts) > 4 and parts[4] else 0
            vel_y = float(parts[5]) if len(parts) > 5 and parts[5] else 0
            ang_x = float(parts[6]) if len(parts) > 6 and parts[6] else 0
            ang_y = float(parts[7]) if len(parts) > 7 and parts[7] else 0
            disp_x = float(parts[2]) if len(parts) > 2 and parts[2] else 0
            disp_y = float(parts[3]) if len(parts) > 3 and parts[3] else 0

            data = {
                'vel_x': vel_x,
                'vel_y': vel_y,
                'disp_x': disp_x,
                'disp_y': disp_y
            }
            self.data_signal.emit(data)

            # Check Danger Logic
            is_danger = False
            if abs(vel_x) > 5 or abs(vel_y) > 5 or abs(ang_x) > 5 or abs(ang_y) > 5:
                is_danger = True
            self.danger_signal.emit(is_danger)

        except (ValueError, IndexError):
            pass  # Ignore malformed lines

    def stop(self):
        self.running = False
        self.wait()


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, cfg=None):
        super().__init__()
        # 只初始化一次UI，删除重复的setupUi调用
        self.setupUi(self)  # 这是唯一的一次UI初始化

        # 强制启用所有按钮（在UI初始化后执行，作用于正确的按钮对象）
        self.pushButton_img.setEnabled(True)
        self.pushButton_dir.setEnabled(True)
        self.pushButton_video.setEnabled(True)
        self.pushButton_camera.setEnabled(True)

        # 以下是其他初始化逻辑，保持不变
        self.frame_number = 0  # 帧计数器
        self.total_frame_count = 0  # Total frames processed (for skipping logic)
        self.comboBox_index = None  # 下拉框当前选中项的索引
        self.results = []  # 存储检测结果
        self.result_img_name = None  # 结果图像文件名

        self.init_UI_config()
        self.start_type = None  # 启动类型
        self.img = None
        self.img_path = None
        self.video = None
        self.video_path = None
        self.img_show = None  # 用于显示的图像副本
        self.sign = True  # 控制循环的标志（如停止检测）

        self.result_info = None  # 存储检测结果信息
        self.csv_data = {'vel_x': 0, 'vel_y': 0, 'disp_x': 0, 'disp_y': 0}  # Store real-time CSV data for UI display

        self.chinese_name = chinese_name  # 中文名称

        self.ProjectPath = os.getcwd()
        self.comboBox_text = '所有目标'
        run_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        self.output_dir = os.path.join(self.ProjectPath, 'output')
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        result_time_path = os.path.join(self.output_dir, run_time)
        os.mkdir(result_time_path)

        self.result_txt = os.path.join(result_time_path, 'result.txt')
        with open(self.result_txt, 'w') as result_file:
            result_file.write(
                str(['编号', '文件名', '输入时间', '识别结果', '目标数量', '耗时', '保存路径', '置信度'])[1:-1])
            result_file.write('\n')

        self.result_img_path = os.path.join(result_time_path, 'img_result')
        os.mkdir(self.result_img_path)

        self.comboBox_value = '所有目标'  ##

        self.number = 1
        self.RowLength = 0
        self.consum_time = 0
        self.input_time = 0

        # 信号与槽绑定（在UI初始化后执行，绑定到正确的按钮对象）
        self.pushButton_img.clicked.connect(self.open_img)
        self.pushButton_dir.clicked.connect(self.open_dir)
        self.pushButton_video.clicked.connect(self.open_video)
        self.pushButton_camera.clicked.connect(self.open_camera)
        self.pushButton_csv.clicked.connect(self.open_csv)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_export.clicked.connect(self.write_files)

        # 下拉框事件绑定
        self.comboBox.activated.connect(self.onComboBoxActivated)
        self.comboBox.mousePressEvent = self.handle_mouse_press

        self.tableWidget_info.cellClicked.connect(self.cell_clicked)

        self.timer = QtCore.QTimer()  # 定时器（用于摄像头/视频帧更新）
        self.timer.timeout.connect(self.update_frame)  # 定时触发帧更新

        self.image_files = []  # 存储批量图片路径
        self.current_index = 0  # 当前图片索引
        self.csv_path = None
        self.csv_thread = None
        self.csv_data = {}  # Store latest CSV data
        self.latest_csv_danger = False  # State to hold the latest danger status

        # Initialize scaling
        self.init_scaling()

    def init_UI_config(self):
        self.setWindowTitle(title)  # 设置窗口标题
        self.label_title.setText(label_title)  # 设置标题标签的文本
        self.setStyleSheet("#centralwidget {background-image: url('%s')}" % background_img)
        self.label_img.setPixmap(QtGui.QPixmap(image2))

        self.label_info.setText(label_info_txt)  # 设置信息标签的文本
        self.label_info.setStyleSheet("color: rgb(%s);" % label_info_color)  # 设置文本颜色

        # 开始按钮样式
        self.pushButton_start.setStyleSheet(
            "background-color: rgb(%s); border-radius: 15px; color: rgb(%s); " % (start_button_bg, start_button_font))
        # 导出按钮样式
        self.pushButton_export.setStyleSheet(
            "background-color: rgb(%s); border-radius: 15px; color: rgb(%s);" % (export_button_bg, export_button_font))

        # 控制区域标签样式（侧边栏）
        self.label_control.setStyleSheet("background-color: rgba(%s); border-radius: 15px;" % label_control_color)
        # 图片显示标签样式
        self.label_img.setStyleSheet("background-color: rgba(%s); border-radius: 15px;" % label_img_color)

        # 设置表格的列头背景色和文字颜色。
        header_style_sheet = """
                    QHeaderView::section {{
                        background-color: rgb({header_background_color});
                        color: {header_color};
                    }}
                    """.format(
            header_background_color=header_background_color,
            header_color=header_color
        )
        self.tableWidget_info.horizontalHeader().setStyleSheet(header_style_sheet)

        # 设置表格整体的背景颜色
        table_widget_info_style_sheet = """
                    QTableWidget {{
                        background-color: rgb({background_color});
                    }}
                    QTableView::item:hover{{
                        background-color:rgb({item_hover_background_color});
                    }}
                    """.format(
            background_color=background_color,
            item_hover_background_color=item_hover_background_color,
        )
        self.tableWidget_info.setStyleSheet(table_widget_info_style_sheet)

        ##
        # 设置表格的每列宽度
        for column, width in enumerate(column_widths):
            # print(column,width)
            self.tableWidget_info.setColumnWidth(column, 111)
        ##

    # 处理用户点击表格某一行时的操作，显示对应检测结果的详细信息
    def cell_clicked(self, row, column):

        self.update_comboBox_default()

        result_info = {}
        # 判断这一行是否有值
        if self.tableWidget_info.item(row, 1) is None:
            return

        self.img_path = self.tableWidget_info.item(row, 1).text()  # 原始图片路径
        self.results = eval(self.tableWidget_info.item(row, 3).text())  # 检测结果列表

        self.result_img_name = self.tableWidget_info.item(row, 6).text()  # 结果图片路径
        self.img_show = cv2.imdecode(np.fromfile(self.result_img_name, dtype=np.uint8), -1)  # 加载结果图片

        # 提取检测结果
        if len(self.results) > 0:
            box = self.results[0][2]
            score = self.results[0][1]
            cls_name = self.results[0][0]
        else:
            box = [0, 0, 0, 0]
            score = 0
            cls_name = 'No Targets'

        # 更新界面
        result_info = result_info_format(result_info, box, score, cls_name)  # 格式化结果显示
        self.get_comboBox_value(self.results)  # 更新下拉框选项
        self.show_all(self.img_show, result_info)  # 显示图片和结果

    # 自定义下拉框的鼠标点击事件，实现动态更新选项
    def handle_mouse_press(self, event):
        ##
        if event.button() == Qt.LeftButton:
            self.comboBox.clear()  # 清空原有选项
            if type(self.comboBox_value) == str:
                self.comboBox_value = [self.comboBox_value]  # 确保是列表格式
            self.comboBox.addItems(self.comboBox_value)  # 添加新选项
        QComboBox.mousePressEvent(self.comboBox, event)  # 保持默认行为

    # 处理选择下拉框选项时的操作，显示筛选后的检测结果
    def onComboBoxActivated(self):

        self.sign = True

        comboBox_text = self.comboBox.currentText()
        self.comboBox_index = self.comboBox.currentIndex()
        result_info = {}

        if len(self.results) == 0:
            print('图片中无目标！')
            QMessageBox.information(self, "提示", "图片中无目标", QMessageBox.Yes)  # 弹出提示框
            return

        if comboBox_text == '所有目标':
            # 显示所有结果
            box = self.results[0][2]
            score = self.results[0][1]
            cls_name = self.results[0][0]
            lst_info = self.results
        else:
            # 利用索引find，显示特定类别结果
            select_result = self.results[self.comboBox_index - 1]
            box = select_result[2]
            cls_name = select_result[0]
            score = select_result[1]
            lst_info = [[cls_name, score, box]]

        # 格式化信息
        result_info = result_info_format(result_info, box, score, cls_name)
        # 重新加载原始图片
        self.img = cv2.imdecode(np.fromfile(self.img_path, dtype=np.uint8), cv2.IMREAD_COLOR)  #
        # 绘制检测框
        self.img_show = draw_info(self.img, lst_info)
        # 更新显示
        self.show_all(self.img_show, result_info)

    # 将图像显示在界面的 label_img 控件上，并自动调整大小和填充
    def show_frame(self, img):
        self.update()  # 强制刷新界面
        if img is not None:
            # 调整图像尺寸并填充颜色（保持宽高比）
            shrink = resize_with_padding(img, self.label_img.width(), self.label_img.height(),
                                         [padvalue[2], padvalue[1], padvalue[0]])  # 目标宽度（控件宽度）  目标高度（控件高度）  填充颜色（BGR格式）
            # 转换颜色通道：OpenCV的BGR -> RGB
            shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
            # 创建QImage对象
            QtImg = QtGui.QImage(shrink[:], shrink.shape[1], shrink.shape[0], shrink.shape[1] * 3,
                                 QtGui.QImage.Format_RGB888)  # 图像数据    宽、高    每行的字节数（宽度*3通道）    RGB格式
            # 显示图像
            self.label_img.setPixmap(QtGui.QPixmap.fromImage(QtImg))

    # 打开单个图片文件，显示路径并预览图像
    def open_img(self):
        try:
            self.update_comboBox_default()  # 重置下拉框
            # 弹出文件选择对话框
            self.img_path, filetype = QFileDialog.getOpenFileName(None, "Img", self.ProjectPath,
                                                                  "JPEG Image (*.jpg);;PNG Image (*.png);;JFIF Image (*.jfif)")
            if self.img_path == "":  # 未选择文件
                self.start_type = None
                return

            # 更新界面路径标签
            self.img_name = os.path.basename(self.img_path)
            #
            self.label_img_path.setText(" " + self.img_path)
            self.label_dir_path.setText(" 文件夹")
            self.label_video_path.setText(" 视频")
            self.label_camera_path.setText(" 摄像头")

            # 标记输入类型为图片
            self.start_type = 'img'
            # 读取路径图片
            self.img = cv2.imdecode(np.fromfile(self.img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            # 显示图片
            self.show_frame(self.img)
        except Exception as e:
            traceback.print_exc()

    # 打开包含图片的文件夹，加载第一张图片并显示
    def open_dir(self):
        try:
            self.update_comboBox_default()
            # 选择文件夹
            self.img_path_dir = QFileDialog.getExistingDirectory(None, "文件夹")
            if not self.img_path_dir:
                self.start_type = None
                return

            # 标记输入类型为文件夹
            self.start_type = 'dir'
            # 更新路径标签
            self.label_dir_path.setText(" " + self.img_path_dir)
            self.label_img_path.setText(" 图片")
            self.label_video_path.setText(" 视频")
            self.label_camera_path.setText(" 摄像头")

            # 获取文件夹内所有支持的图片文件
            self.image_files = [file for file in os.listdir(self.img_path_dir) if file.lower().endswith(
                ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))]

            # 无有效图片
            if not self.image_files:
                QMessageBox.information(self, "提示：", "文件夹中没有符合条件的图像", QMessageBox.Yes)
                return

            # 从第一张开始
            self.current_index = 0
            self.img_path = os.path.join(self.img_path_dir, self.image_files[self.current_index])
            self.img_name = self.image_files[self.current_index]

            self.img = cv2.imdecode(np.fromfile(self.img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
            self.show_frame(self.img)
        except Exception as e:
            traceback.print_exc()

    def open_video(self):
        try:
            # 更新下拉列表的状态
            self.update_comboBox_default()
            # 选择视频文件
            self.video_path, filetype = QFileDialog.getOpenFileName(None, "Video", self.ProjectPath,
                                                                    "mp4 Video (*.mp4);;avi Video (*.avi)")
            if not self.video_path:
                self.start_type = None
                return

            # 标记输入类型为视频
            self.start_type = 'video'
            # 更新路径标签
            self.label_video_path.setText(" " + self.video_path)
            self.label_img_path.setText(" 图片")
            self.label_dir_path.setText(" 文件夹")
            self.label_camera_path.setText(" 摄像头")

            self.video_name = os.path.basename(self.video_path)
            self.video = cv2.VideoCapture(self.video_path)  # 初始化视频捕获对象
            # 读取第一帧
            ret, self.img = self.video.read()
            self.show_frame(self.img)
        except Exception as e:
            traceback.print_exc()

    # 打开摄像头，显示实时画面
    def open_camera(self):
        try:
            self.update_comboBox_default()
            # 初始状态：标签文本是“ 摄像头”（未开启）
            if self.label_camera_path.text() in [' 摄像头', ' 摄像头关闭']:
                self.start_type = 'camera'
                # 更新标签为“已开启”
                self.label_img_path.setText(" 图片")
                self.label_dir_path.setText(" 文件夹")
                self.label_video_path.setText(" 视频")
                self.label_camera_path.setText(" 摄像头开启")

                # 尝试打开摄像头（先试编号0，失败再试1）
                self.video = cv2.VideoCapture(camera_num)
                if not self.video.isOpened():  # 若编号0失败，尝试编号1
                    self.video = cv2.VideoCapture(1)
                    if not self.video.isOpened():  # 仍失败则提示
                        QMessageBox.warning(self, "错误", "无法打开摄像头，请检查设备连接！", QMessageBox.Yes)
                        return

                self.video_name = f"camera_{camera_num}"
                # 读取并显示第一帧
                ret, self.img = self.video.read()
                if ret:
                    self.show_frame(self.img)
                else:
                    QMessageBox.warning(self, "错误", "无法读取摄像头画面！", QMessageBox.Yes)

            # 已开启状态：点击按钮关闭摄像头
            elif self.label_camera_path.text() == ' 摄像头开启':
                # 恢复按钮文本和标签状态
                self.pushButton_start.setText("运行 >")
                self.label_camera_path.setText(" 摄像头关闭")
                # 释放摄像头资源
                if self.video is not None and self.video.isOpened():
                    self.video.release()
                # 清空显示画面（可选）
                self.label_img.setPixmap(QtGui.QPixmap(image2))  # 显示默认图片

        except Exception as e:
            traceback.print_exc()
            # 异常时释放资源
            if self.video is not None and self.video.isOpened():
                self.video.release()
            self.label_camera_path.setText(" 摄像头关闭")

    def open_csv(self):
        try:
            self.update_comboBox_default()
            self.csv_path, filetype = QFileDialog.getOpenFileName(None, "CSV", self.ProjectPath, "CSV (*.csv)")
            if not self.csv_path:
                self.start_type = None
                return
            self.label_csv_path.setText(" " + self.csv_path)
            self.label_img_path.setText(" 图片")
            self.label_dir_path.setText(" 文件夹")
            self.label_video_path.setText(" 视频")
            self.label_camera_path.setText(" 摄像头")

            # If camera is already selected, keep it as camera (combination mode)
            if self.start_type != 'camera':
                self.start_type = 'csv'
        except Exception as e:
            traceback.print_exc()

    def show_all(self, img, info):
        self.show_frame(img)  # 显示图像
        self.show_info(info)  # 显示检测结果信息

    def on_csv_data_update(self, data):
        self.csv_data = data
        # Update UI immediately for smooth data display
        try:
            self.label_xmin_v.setText(str(data.get('vel_x', 0)))
            self.label_ymin_v.setText(str(data.get('vel_y', 0)))
            self.label_xmax_v.setText(str(data.get('disp_x', 0)))
            self.label_ymax_v.setText(str(data.get('disp_y', 0)))
        except Exception:
            pass

    def on_danger_update(self, is_danger):
        self.latest_csv_danger = is_danger

    """
        A[start] --> B{输入类型}
        B -->|图片| C[读取图片并检测]
        B -->|文件夹/视频/摄像头| D{按钮状态}
        D -->|运行| E[启动定时器]
        D -->|停止| F[停止定时器并释放资源]
        E --> G[定时触发update_frame]
        G --> H{输入类型}
        H -->|文件夹| I[加载下一张图片]
        H -->|视频/摄像头| J[读取下一帧]
        I/J --> K[目标检测]
        K --> L[显示结果]
        """

    def start(self):
        # 重置下拉框到默认状态
        self.update_comboBox_default()
        try:
            # 检查是否已选择输入类型
            if self.start_type == None:
                QMessageBox.information(self, "提示", "请先选择输入类型！", QMessageBox.Yes)
                return
            # 处理图片输入
            if self.start_type == 'img':
                # 从路径读取图片
                self.img = cv2.imdecode(np.fromfile(self.img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
                # 进行目标检测，返回结果图像和详细信息
                _, result_info = self.predict_img(self.img)
                # 显示结果图像和信息
                self.show_all(self.img_show, result_info)

            # 处理文件夹、视频、摄像头输入
            elif self.start_type in ['dir', 'video', 'camera']:
                # 根据按钮文本判断当前状态（启动或停止）
                if self.pushButton_start.text() == '运行 >':

                    # Initialize CSV reading thread if path is set
                    if self.csv_path and os.path.exists(self.csv_path):
                        try:
                            if self.csv_thread is not None:
                                self.csv_thread.stop()
                            self.csv_thread = CSVReaderThread(self.csv_path)
                            self.csv_thread.data_signal.connect(self.on_csv_data_update)
                            self.csv_thread.danger_signal.connect(self.on_danger_update)
                            self.csv_thread.start()
                        except Exception as e:
                            print(f"Error starting CSV thread: {e}")

                    # Reset danger state on start
                    self.latest_csv_danger = False

                    self.timer.start(20)  # 每20毫秒处理一张图片或一帧
                    # 更新按钮文本为“结束操作”
                    self.pushButton_start.setText("运行结束 >")
                    # 摄像头模式下更新路径标签
                    if self.start_type == 'camera':
                        self.label_camera_path.setText(" 摄像头开启")
                # 如果当前是运行状态，则停止
                elif self.pushButton_start.text() == '运行结束 >':
                    # 恢复按钮文本
                    self.pushButton_start.setText("运行 >")
                    # 停止定时器
                    self.timer.stop()

                    # Stop CSV thread
                    if self.csv_thread:
                        self.csv_thread.stop()
                        self.csv_thread = None

                    # 摄像头模式下释放资源并更新标签
                    if self.start_type == 'camera' and self.video is not None and self.video.isOpened():
                        self.video.release()
                        self.label_camera_path.setText(" 摄像头关闭")
        except Exception:
            traceback.print_exc()

        if self.start_type == 'csv':
            try:
                _, result_info = self.predict_csv(self.csv_path)
                self.show_all(None, result_info)
            except Exception:
                traceback.print_exc()

    def update_frame(self):
        # 处理文件夹输入
        if self.start_type == 'dir':
            # 检查是否处理完所有图片
            if self.current_index >= len(self.image_files):
                # 停止定时器并重置状态
                self.pushButton_start.setText("运行 >")
                self.timer.stop()
                self.frame_number = 0  # 重置帧计数器
                # 弹出完成提示
                if self.current_index >= len(self.image_files):
                    QMessageBox.information(self, "提示", "此文件夹已识别完毕", QMessageBox.Yes)
                return

            # 获取下一张图片的路径
            self.img_name = self.image_files[self.current_index]
            self.img_path = os.path.join(self.img_path_dir, self.img_name)
            # 读取图片
            self.img = cv2.imdecode(np.fromfile(self.img_path, dtype=np.uint8), -1)
            # 更新索引以处理下一张
            self.current_index += 1

        # 处理视频或摄像头输入
        elif self.start_type in ['video', 'camera']:
            # 视频模式下重置到第一帧（仅在首次运行时触发）
            if self.frame_number == 0 and self.start_type == 'video':
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 设置视频帧位置为起始
                ret, self.img = self.video.read()  # 读取第一帧
                if ret:
                    # 获取当前帧编号并生成文件名
                    frame_number = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                    self.img_name = f"{self.video_name}_{frame_number}.jpg"
                    self.img_path = self.video_path
                    self.frame_number = 0  # 重置帧计数器
                else:
                    # 视频读取失败，停止并释放资源
                    self.pushButton_start.setText("运行 >")
                    self.timer.stop()
                    self.video.release()
                    self.frame_number = 0
                    QMessageBox.information(self, "提示", "视频已识别完毕", QMessageBox.Yes)
                    return
            else:
                # 读取下一帧
                ret, self.img = self.video.read()
                if not ret:  # 无更多帧
                    self.pushButton_start.setText("运行 >")
                    self.timer.stop()
                    self.video.release()
                    self.frame_number = 0
                    # 根据输入类型弹出不同提示
                    if self.start_type == 'video':
                        QMessageBox.information(self, "提示", "视频已识别完毕", QMessageBox.Yes)
                    elif self.start_type == 'camera':
                        self.label_camera_path.setText(" 摄像头关闭")
                        QMessageBox.information(self, "提示", "摄像头关闭", QMessageBox.Yes)
                    return
                # 生成帧文件名（视频按帧编号，摄像头按计数器）
                if self.start_type == 'video':
                    frame_number = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
                    self.img_name = f"{self.video_name}_{frame_number}.jpg"
                    self.img_path = self.video_path
                elif self.start_type == 'camera':
                    self.frame_number += 1
                    self.img_name = f"camera_{self.frame_number}.jpg"
                    self.img_path = 'camera'  # 标记为摄像头输入

        self.total_frame_count += 1

        # Optimization: Skip YOLO detection on some frames to unblock UI and CSV updates
        # Process 1 out of every 3 frames (adjust if needed)
        if self.total_frame_count % 3 != 0 and self.results:
            # Use previous results to draw boxes on new frame (Persistence)
            self.img_show = draw_info(self.img, self.results)
        else:
            # Perform Object Detection
            self.results, self.result_info = self.predict_img(self.img)

        # ---------------------------------------------------------
        # Combine CSV Data and Camera Detection for Fatigue Warning
        # ---------------------------------------------------------
        # Note: CSV reading is now handled by CSVReaderThread updates self.latest_csv_danger
        csv_danger = self.latest_csv_danger

        camera_fatigue = False
        if self.results:
            for res in self.results:
                cls_name = res[0]
                # Check for fatigue indicators (Closed Eye, Open Mouth/Yawn)
                if cls_name in ['closed_eye', 'open_mouth', '闭眼', '张嘴']:
                    camera_fatigue = True
                    break

        # Display Status on Screen (Help user understand state)
        # Vehicle Status
        v_color = (0, 0, 255) if csv_danger else (0, 255, 0)
        v_text = "Vehicle: DANGER" if csv_danger else "Vehicle: Safe"
        cv2.putText(self.img_show, v_text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, v_color, 2)

        # Driver Status
        d_color = (0, 0, 255) if camera_fatigue else (0, 255, 0)
        d_text = "Driver: FATIGUE" if camera_fatigue else "Driver: Normal"
        cv2.putText(self.img_show, d_text, (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, d_color, 2)

        # Trigger Warning if BOTH conditions are met
        if csv_danger and camera_fatigue:
            # Visual Warning
            cv2.putText(self.img_show, "WARNING: FATIGUE DRIVING!", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                        (0, 0, 255), 3)
            # Voice Warning
            try:
                # Run beep in a separate thread to prevent blocking
                threading.Thread(target=lambda: winsound.Beep(1000, 200)).start()
                print("当前为疲劳驾驶 (Fatigue Driving Detected)")
            except:
                pass
        # ---------------------------------------------------------

        # 显示结果图像和信息
        # If we skipped detection, self.result_info might be from previous frame, which is fine
        if self.result_info:
            self.show_all(self.img_show, self.result_info)
        else:
            self.show_frame(self.img_show)

        if self.start_type == 'video':
            self.frame_number += 1

        """
        A[predict_img] -->|调用| B[YOLO预测]
        A -->|生成结果| C[保存图像和文本]
        A -->|更新界面| D[show_table]
        A -->|更新下拉框| E[get_comboBox_value]
        D --> F[表格插入行]
        G[write_files] -->|读取结果| H[文本文件]
        G -->|导出数据| I[Excel/CSV]
        """

    def predict_img(self, img):
        # 初始化结果信息字典
        result_info = {}
        # 记录开始时间（用于计算处理耗时）
        t1 = time.time()
        # 生成结果图像的保存路径
        self.result_img_name = os.path.join(self.result_img_path, self.img_name)

        # 调用 YOLO 模型进行预测
        # imgsz: 输入图像尺寸
        # conf_thres: 置信度阈值
        # device: 计算设备
        # classes: 允许检测的类别
        self.results = yolo.predict(img, imgsz=imgsz, conf=conf_thres, device=device, classes=classes)
        # 格式化检测结果
        self.results = format_data(self.results)

        # 计算处理时间并转换为字符串（保留两位小数）
        self.consum_time = str(round(time.time() - t1, 2)) + 's'

        # 记录当前时间作为输入时间
        self.input_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ## 写置信度
        confidences = []
        if self.results is not None:
            for result in self.results:
                if len(result) >= 2:
                    confidences.append(result[1])
        # 将结果写入文本文件
        with open(self.result_txt, 'a+') as result_file:
            # 写入格式：ID, 图片路径, 输入时间, 检测结果, 目标数量, 耗时, 结果图片路径,置信度
            result_file.write(
                str([self.number, self.img_path, self.input_time, self.results, len(self.results), self.consum_time,
                     self.result_img_name, confidences])[1:-1])
            result_file.write('\n')
        # 更新表格显示
        self.show_table()
        # 自增结果ID（用于下一条记录）
        self.number += 1
        # 更新下拉框选项（显示检测到的类别）
        self.get_comboBox_value(self.results)

        # 提取第一个检测结果（用于主界面显示）
        if len(self.results) > 0:
            box = self.results[0][2]  # 检测框坐标 [x1, y1, x2, y2]
            score = self.results[0][1]  # 置信度
            cls_name = self.results[0][0]  # 类别名称
        else:
            # 如果无识别结果，设置默认值
            box = [0, 0, 0, 0]
            score = 0
            cls_name = 'No Targets'

        # 格式化结果信息（填充字典）
        result_info = result_info_format(result_info, box, score, cls_name)
        # 在图像上绘制检测框和标签(同一类型结果也会用不同颜色标注)
        self.img_show = draw_info(img, self.results)
        # 保存结果图像
        cv2.imencode('.jpg', self.img_show)[1].tofile(self.result_img_name)

        return self.results, result_info

    def predict_csv(self, path):
        result_info = {}
        t1 = time.time()
        self.img_name = os.path.basename(path)
        self.results = [['平稳驾驶', 1.0, [0, 0, 0, 0]]]
        self.consum_time = str(round(time.time() - t1, 2)) + 's'
        self.input_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        confidences = [r[1] for r in self.results]
        with open(self.result_txt, 'a+') as result_file:
            result_file.write(
                str([self.number, path, self.input_time, self.results, len(self.results), self.consum_time,
                     '', confidences])[1:-1])
            result_file.write('\n')
        self.show_table()
        self.number += 1
        self.get_comboBox_value(self.results)
        box = self.results[0][2]
        score = self.results[0][1]
        cls_name = self.results[0][0]
        result_info = result_info_format(result_info, box, score, cls_name)
        self.img_show = None
        return self.results, result_info

    # 根据检测结果生成下拉框的选项列表
    # 例如，检测到 ['scratch', 'oxidize']，则下拉框选项为 ['All Targets', 'scratch', 'oxidize']
    # 用于在界面中选择显示特定类别的结果
    def get_comboBox_value(self, results):
        lst = ["All Targets"]  # 默认包含“全部目标”
        for bbox in results:
            cls_name = bbox[0]  # 提取类别名称
            lst.append(str(cls_name))  # 添加到列表
        self.comboBox_value = lst  # 存储为类属性

    # 在界面标签中显示单个目标的详细信息
    def show_info(self, result):
        try:
            if len(result) == 0:  # 空结果处理
                print("无目标")
                return
            # 获取类别名称，先判断是否在中文映射中
            cls_name = result['cls_name']
            # 关键修改：如果cls_name不在chinese_name中，直接使用原名称（如'No Targets'）
            if cls_name in self.chinese_name:
                cls_name = self.chinese_name[cls_name]
            else:
                cls_name = cls_name  # 或设为中文“无目标”，如 cls_name = "无目标"

            # 处理长类别名称（截断显示）
            if len(cls_name) > 10:
                lst_cls_name = cls_name.split('_')
                cls_name = lst_cls_name[0][:10] + '...'

            # 更新界面标签
            self.label_class.setText(str(cls_name))  # 类别
            self.label_score.setText(str(result['score']))  # 置信度
            # self.label_xmin_v.setText(str(result['label_xmin_v']))  # 框左上角x
            # self.label_ymin_v.setText(str(result['label_ymin_v']))  # 框左上角y
            # self.label_xmax_v.setText(str(result['label_xmax_v']))  # 框右上角x
            # self.label_ymax_v.setText(str(result['label_ymax_v']))  # 框右上角y

            # Display Real-time CSV Data (Speed/Displacement)
            # Use .get() with default 0 to prevent errors
            self.label_xmin_v.setText(str(self.csv_data.get('vel_x', 0)))
            self.label_ymin_v.setText(str(self.csv_data.get('vel_y', 0)))
            self.label_xmax_v.setText(str(self.csv_data.get('disp_x', 0)))
            self.label_ymax_v.setText(str(self.csv_data.get('disp_y', 0)))

            self.update()  # 刷新界面
        except Exception as e:
            traceback.print_exc()

    # 重置下拉框到默认状态（仅显示“All Targets”）
    def update_comboBox_default(self):
        self.comboBox.clear()  # 清空所有选项
        self.comboBox.addItems([self.comboBox_text])  # 添加默认文本（'All Targets'）

    # 在表格控件中插入一行新的检测结果
    def show_table(self):
        try:
            # 增加行数
            self.RowLength = self.RowLength + 1
            self.tableWidget_info.setRowCount(self.RowLength)
            # 遍历要显示的字段：ID, 路径, 时间, 结果, 数量, 耗时, 结果图路径 ,置信度
            ##展示置信度
            confidences = []
            if self.results is not None:
                for result in self.results:
                    if len(result) >= 2:
                        confidences.append(result[1])
            ##

            for column, content in enumerate(
                    [self.number, self.img_path, self.input_time, self.results, len(self.results), self.consum_time,
                     self.result_img_name, confidences]):
                row = self.RowLength - 1  # 当前行索引
                item = QtWidgets.QTableWidgetItem(str(content))  # 创建表格项
                item.setTextAlignment(QtCore.Qt.AlignCenter)  # 居中显示
                item.setForeground(QColor.fromRgb(column_color[0], column_color[1], column_color[2]))  # 设置文字颜色（从配置读取）
                self.tableWidget_info.setItem(row, column, item)  # 插入单元格
            self.tableWidget_info.scrollToBottom()  # 滚动到底部
        except Exception as e:
            traceback.print_exc()

    # 将检测结果导出为 Excel 或 CSV 文件
    def write_files(self):
        # 弹出保存对话框
        path, filetype = QFileDialog.getSaveFileName(None, "Save as", self.ProjectPath,
                                                     "Excel 工作簿(*.xls);;CSV (逗号分隔)(*.csv)")
        # 读取结果文本文件
        with open(self.result_txt, 'r') as f:
            lst_txt = f.readlines()
            # 将每行文本转换为列表
            data = [list(eval(x.replace('\n', ''))) for x in lst_txt]

        if path == "":  # 用户取消保存
            return
        # 根据选择的文件类型调用不同写入函数
        if filetype == 'Excel 工作簿(*.xls)':
            writexls(data, path)
        elif filetype == 'CSV (逗号分隔)(*.csv)':
            writecsv(data, path)
        # 提示保存成功
        QMessageBox.information(None, "成功保存", "数据已保存！", QMessageBox.Yes)

    # --- Scaling Logic ---
    def init_scaling(self):
        self.base_width = 1264
        self.base_height = 896
        self.widget_initial_states = {}

        # Capture all direct children of centralwidget for scaling
        all_widgets = self.centralwidget.findChildren(QtWidgets.QWidget)
        for widget in all_widgets:
            # Skip widgets that are children of complex controls to avoid breaking internal layouts
            parent = widget.parent()
            if isinstance(parent, (QtWidgets.QTableWidget, QtWidgets.QComboBox)):
                continue

            # Skip internal components
            if isinstance(widget, (QtWidgets.QScrollBar, QtWidgets.QHeaderView)):
                continue

            self.widget_initial_states[widget] = {
                'rect': widget.geometry(),
                'font_size': widget.font().pointSize()
            }

        # Capture column widths
        self.initial_column_widths = []
        for i in range(self.tableWidget_info.columnCount()):
            self.initial_column_widths.append(self.tableWidget_info.columnWidth(i))

    def resizeEvent(self, event):
        self.apply_scaling()
        super().resizeEvent(event)

    def apply_scaling(self):
        if not hasattr(self, 'widget_initial_states'):
            return

        # Calculate scale factors
        current_width = self.width()
        current_height = self.height()

        # Avoid division by zero
        if self.base_width == 0 or self.base_height == 0:
            return

        scale_x = current_width / self.base_width
        scale_y = current_height / self.base_height
        scale_font = min(scale_x, scale_y)

        for widget, state in self.widget_initial_states.items():
            try:
                # Scale Geometry
                rect = state['rect']
                new_x = int(rect.x() * scale_x)
                new_y = int(rect.y() * scale_y)
                new_w = int(rect.width() * scale_x)
                new_h = int(rect.height() * scale_y)
                widget.setGeometry(new_x, new_y, new_w, new_h)

                # Scale Font
                if state['font_size'] > 0:
                    font = widget.font()
                    new_size = max(1, int(state['font_size'] * scale_font))
                    font.setPointSize(new_size)
                    widget.setFont(font)
            except Exception:
                pass  # Widget might have been deleted

        # Scale Table Columns
        for i, width in enumerate(self.initial_column_widths):
            self.tableWidget_info.setColumnWidth(i, int(width * scale_x))


if __name__ == "__main__":
    # 加载配置，初始化模型，设置并启动GUI应用程序
    # GUI会使用配置中的各种参数来自定义外观，而模型部分使用YOLO进行目标检测，在GUI中实时显示检测结果，可以处理图像/视频输入
    # path_cfg = 'D:/作业/传感器/汇报ppt/ultralytics-main/ultralytics-main/1.yml'
    path_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), '1.yml')
    cfg = get_config()
    cfg.merge_from_file(path_cfg)
    cfg_model = cfg.MODEL
    weights = cfg_model.WEIGHT
    conf_thres = float(cfg_model.CONF)  # 置信阈值
    classes = eval(cfg_model.CLASSES)  # 检测类别列表
    imgsz = int(cfg_model.IMGSIZE)  # img_size
    device = cfg_model.DEVICE
    # 加载UI界面相关的配置
    cfg_UI = cfg.UI
    background_img = cfg_UI.background  # 背景图片
    padvalue = cfg_UI.padvalue  # 布局填充值
    column_widths = cfg_UI.column_widths  # 列宽
    column_color = cfg_UI.column_color  # 列颜色
    title = cfg_UI.title  # 标题
    label_title = cfg_UI.label_title  # label标题
    image2 = cfg_UI.image2  # image2
    label_info_txt = cfg_UI.label_info_txt  # label txt
    label_info_color = cfg_UI.label_info_color  # label color
    start_button_bg = cfg_UI.start_button_bg
    start_button_font = cfg_UI.start_button_font
    export_button_bg = cfg_UI.export_button_bg
    export_button_font = cfg_UI.export_button_font
    label_control_color = cfg_UI.label_control_color
    label_img_color = cfg_UI.label_img_color
    header_background_color = cfg_UI.table_widget_info_styles.header_background_color
    header_color = cfg_UI.table_widget_info_styles.header_color
    background_color = cfg_UI.table_widget_info_styles.background_color
    item_hover_background_color = cfg_UI.table_widget_info_styles.item_hover_background_color

    camera_num = int(cfg.CONFIG.camera_num)
    chinese_name = cfg.CONFIG.chinese_name

    yolo = YOLO(weights)
    yolo.predict(np.zeros((300, 300, 3), dtype='uint8'), device=device)  # 预热推理，提前初始化模型

    app = QApplication([])
    window = MyMainWindow(cfg)
    window.show()
    app.exec_()