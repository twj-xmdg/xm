import torch
from ultralytics import YOLO
model = YOLO("yolo11n.pt")
results = model("img.png")
results[0].show()

import torch
print(torch.cuda.is_available())  # 应返回 True
print(torch.cuda.get_device_name(0))  # 显示你的 NVIDIA 显卡型号

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading
import time


class FatigueDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("疲劳驾驶检测系统")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # 模型相关
        self.model = None
        self.class_names = ['normal', 'closed_eye', 'yawning']  # 对应你的类别
        self.conf_threshold = 0.5  # 置信度阈值

        # 视频相关
        self.video_path = None
        self.cap = None
        self.running = False
        self.detection_thread = None

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 顶部按钮区域
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X, padx=20)

        # 模型加载按钮
        self.model_path_var = tk.StringVar(value="未加载模型")
        model_btn = tk.Button(top_frame, text="加载模型", command=self.load_model)
        model_btn.pack(side=tk.LEFT, padx=5)
        model_label = tk.Label(top_frame, textvariable=self.model_path_var, width=40)
        model_label.pack(side=tk.LEFT, padx=5)

        # 置信度调整
        conf_frame = tk.Frame(top_frame)
        conf_frame.pack(side=tk.RIGHT, padx=5)
        tk.Label(conf_frame, text="置信度阈值:").pack(side=tk.LEFT)
        self.conf_scale = tk.Scale(conf_frame, from_=0.1, to=1.0, resolution=0.1,
                                   orient=tk.HORIZONTAL, length=150, command=self.update_conf)
        self.conf_scale.set(self.conf_threshold)
        self.conf_scale.pack(side=tk.LEFT)
        self.conf_label = tk.Label(conf_frame, text=f"{self.conf_threshold:.1f}")
        self.conf_label.pack(side=tk.LEFT, padx=5)

        # 视频选择区域
        video_frame = tk.Frame(self.root)
        video_frame.pack(pady=10, fill=tk.X, padx=20)

        self.video_path_var = tk.StringVar(value="未选择视频")
        video_btn = tk.Button(video_frame, text="选择视频", command=self.select_video)
        video_btn.pack(side=tk.LEFT, padx=5)
        video_label = tk.Label(video_frame, textvariable=self.video_path_var, width=60)
        video_label.pack(side=tk.LEFT, padx=5)

        # 控制按钮区域
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        self.start_btn = tk.Button(control_frame, text="开始检测", command=self.start_detection, width=15)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        self.pause_btn = tk.Button(control_frame, text="暂停", command=self.pause_detection, width=15,
                                   state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=10)
        self.stop_btn = tk.Button(control_frame, text="停止", command=self.stop_detection, width=15, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)

        # 视频显示区域
        self.display_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        self.display_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        self.video_label = tk.Label(self.display_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # 状态显示区域
        self.status_var = tk.StringVar(value="状态: 就绪")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_model(self):
        """加载训练好的模型"""
        model_path = filedialog.askopenfilename(
            title="选择模型文件",
            filetypes=[("PyTorch模型", "*.pt")]
        )
        if not model_path:
            return

        try:
            self.model = YOLO(model_path)
            self.model_path_var.set(model_path.split("/")[-1])  # 显示文件名
            self.status_var.set(f"状态: 模型加载成功")
            messagebox.showinfo("成功", "模型加载成功！")
        except Exception as e:
            self.status_var.set(f"状态: 模型加载失败")
            messagebox.showerror("错误", f"加载模型时出错: {str(e)}")

    def select_video(self):
        """选择本地视频文件"""
        video_path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv")]
        )
        if video_path:
            self.video_path = video_path
            self.video_path_var.set(video_path.split("/")[-1])  # 显示文件名
            self.status_var.set(f"状态: 已选择视频")

    def update_conf(self, value):
        """更新置信度阈值"""
        self.conf_threshold = float(value)
        self.conf_label.config(text=f"{self.conf_threshold:.1f}")

    def start_detection(self):
        """开始视频检测"""
        if not self.model:
            messagebox.showwarning("警告", "请先加载模型！")
            return

        if not self.video_path:
            # 如果未选择视频，默认使用摄像头
            self.cap = cv2.VideoCapture(0)
            self.video_path_var.set("摄像头实时画面")
        else:
            self.cap = cv2.VideoCapture(self.video_path)

        if not self.cap.isOpened():
            messagebox.showerror("错误", "无法打开视频源！")
            return

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("状态: 正在检测...")

        # 启动检测线程
        self.detection_thread = threading.Thread(target=self.process_video)
        self.detection_thread.daemon = True
        self.detection_thread.start()

    def pause_detection(self):
        """暂停检测"""
        if self.running:
            self.running = False
            self.pause_btn.config(text="继续")
            self.status_var.set("状态: 已暂停")
        else:
            self.running = True
            self.pause_btn.config(text="暂停")
            self.status_var.set("状态: 正在检测...")
            # 重新启动线程
            self.detection_thread = threading.Thread(target=self.process_video)
            self.detection_thread.daemon = True
            self.detection_thread.start()

    def stop_detection(self):
        """停止检测"""
        self.running = False
        if self.cap:
            self.cap.release()
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="暂停")
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("状态: 已停止")
        self.video_label.config(image="")  # 清空显示

    def process_video(self):
        """处理视频帧并进行检测"""
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.status_var.set("状态: 视频结束")
                self.running = False
                break

            # 用模型进行检测
            results = self.model(frame, conf=self.conf_threshold)

            # 绘制检测结果
            annotated_frame = results[0].plot()

            # 转换为Tkinter可用的格式
            frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)

            # 调整图像大小以适应窗口
            window_width = self.display_frame.winfo_width()
            window_height = self.display_frame.winfo_height()
            if window_width > 10 and window_height > 10:  # 确保窗口已初始化
                img.thumbnail((window_width, window_height))

            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.config(image=imgtk)

            # 控制帧率（避免过高占用CPU）
            time.sleep(0.01)

        # 检测结束后释放资源
        if self.cap:
            self.cap.release()


if __name__ == "__main__":
    root = tk.Tk()
    app = FatigueDetectionApp(root)
    root.mainloop()