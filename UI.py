from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)  # 非模态窗口
        MainWindow.setEnabled(True)
        MainWindow.resize(1264, 896)  # 初始窗口大小
        # MainWindow.setMinimumSize(QtCore.QSize(1264, 896)) # Removed fixed size constraints
        # MainWindow.setMaximumSize(QtCore.QSize(1264, 896)) # Removed fixed size constraints
        font = QtGui.QFont()
        font.setFamily("仿宋")
        MainWindow.setFont(font)  # 将字体家族设置为 “仿宋”
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)  # 将创建的字体应用到主窗口
        MainWindow.setAutoFillBackground(False)  # 设置窗口的上下文菜单策略为默认，允许显示默认的上下文菜单
        # 背景图片通过 CSS 样式设置，路径为 ./icon/czy_background.png
        MainWindow.setStyleSheet("#centralwidget {background-image: url(\"./icon/czy_background.png\");}\n"
                                 "\n"
                                 "")  # 背景图

        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Chinese, QtCore.QLocale.China))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()  # 创建centralwidget部件
        font.setFamily("黑体")
        self.centralwidget.setFont(font)
        self.centralwidget.setObjectName("centralwidget")
        self.label_title = QtWidgets.QLabel(self.centralwidget)  # 创建一个QLabel控件，显示标题
        self.label_title.setGeometry(QtCore.QRect(120, 22, 1011, 61))  # 设置标题标签的位置和大小，位置在窗口的(120,22)处，宽度1011，高度61
        self.label_title.setMinimumSize(QtCore.QSize(0, 0))  # 设置标题标签的最小尺寸为0x0，允许缩放
        self.label_title.setMaximumSize(QtCore.QSize(10000, 10000))  # 设置标题标签的最大尺寸为10000x10000
        font = QtGui.QFont()  # 创建一个新的字体对象，用于设置标题标签的字体
        font.setFamily("微软雅黑")
        font.setPointSize(30)  # 将字体大小设置为30点
        font.setBold(True)  # 将字体设置为加粗
        font.setItalic(False)  # 将字体设置为非斜体
        font.setWeight(75)  # 设置字体的权重为75，进一步加粗字体
        self.label_title.setFont(font)  # 字体：微软雅黑，30号，加粗
        self.label_title.setStyleSheet("color: rgb(255, 255, 255);")  # 设置标题标签的文本颜色为RGB(155,15,255)，即紫色 (过去式)
        self.label_title.setScaledContents(True)  # 允许标题标签根据尺寸缩放内容
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)  # 将标题标签的文本对齐方式设置为居中
        self.label_title.setObjectName("label_title")  # 设置标题标签的对象名称
        self.frame = QtWidgets.QFrame(self.centralwidget)  # 创建一个QFrame控件，用于显示一条水平线
        self.frame.setGeometry(QtCore.QRect(257, 90, 721, 20))  # 设置水平线的位置和大小，位置在(257,90)，宽度721，高度20
        font = QtGui.QFont()  # 创建一个新的字体对象，用于设置水平线的字体
        font.setPointSize(9)  # 将字体大小设置为9点
        self.frame.setFont(font)  # 将创建的字体应用到水平线
        self.frame.setAcceptDrops(True)  # 允许水平线接受拖放事件
        self.frame.setToolTipDuration(-2)  # 设置工具提示的显示时间为-2，表示使用默认值
        self.frame.setFrameShape(QtWidgets.QFrame.HLine)  # 水平线
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)  # 设置水平线的阴影效果为凸起
        self.frame.setLineWidth(1)  # 设置水平线的宽度为1像素
        self.frame.setObjectName("frame")  # 设置水平线的对象名称
        self.label_img = QtWidgets.QLabel(self.centralwidget)  # 创建一个QLabel控件，用于显示图片
        self.label_img.setGeometry(QtCore.QRect(350, 150, 891, 501))  # 设置图片标签的位置和大小，位置在(350,150)，宽度891，高度501
        self.label_img.setStyleSheet("background-color: rgba(48, 52, 152, 100);\n"
                                     "border-radius: 15px;\n"  # 设置图片标签的样式，背景颜色为半透明的RGB(181,194,43)，边界圆角半径为15px
                                     "")  # 122 135 154 150  副图背景
        self.label_img.setText("")  # 设置图片标签的文本为空
        self.label_img.setPixmap(QtGui.QPixmap("icon/YuanShen.png"))  # 设置图片标签显示的图片
        self.label_img.setAlignment(QtCore.Qt.AlignCenter)  # 将图片标签的内容对齐方式设置为居中
        self.label_img.setWordWrap(False)  # 禁止图片标签的文本自动换行
        self.label_img.setIndent(-1)  # 设置文本缩进为-1，表示没有缩进
        self.label_img.setOpenExternalLinks(False)  # 禁止图片标签中的链接打开外部浏览器
        self.label_img.setObjectName("label_img")  # 设置图片标签的对象名称
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(35, 725, 40, 40))
        self.label_17.setText("")
        self.label_17.setPixmap(QtGui.QPixmap("icon/Position.png"))
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(85, 730, 120, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_9.setObjectName("label_9")
        self.label_xmin = QtWidgets.QLabel(self.centralwidget)
        self.label_xmin.setGeometry(QtCore.QRect(30, 780, 80, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_xmin.setFont(font)
        self.label_xmin.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_xmin.setObjectName("label_xmin")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(190, 780, 80, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20.setGeometry(QtCore.QRect(30, 830, 80, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_20.setFont(font)
        self.label_20.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21.setGeometry(QtCore.QRect(190, 830, 80, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_21.setFont(font)
        self.label_21.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_21.setObjectName("label_21")
        self.label_23 = QtWidgets.QLabel(self.centralwidget)
        self.label_23.setGeometry(QtCore.QRect(250, 197, 50, 27))
        self.label_23.setText("")
        self.label_23.setPixmap(QtGui.QPixmap("icon2/Targets_num.png"))
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.label_24 = QtWidgets.QLabel(self.centralwidget)
        self.label_24.setGeometry(QtCore.QRect(260, 240, 30, 30))
        self.label_24.setText("")
        self.label_24.setPixmap(QtGui.QPixmap("icon2/Targets.png"))
        self.label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.label_24.setObjectName("label_24")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(30, 360, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setLineWidth(1)
        self.frame_3.setObjectName("frame_3")
        self.frame_6 = QtWidgets.QFrame(self.centralwidget)
        self.frame_6.setGeometry(QtCore.QRect(30, 570, 301, 20))
        font = QtGui.QFont()
        font.setPointSize(2)
        self.frame_6.setFont(font)
        self.frame_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setLineWidth(1)
        self.frame_6.setMidLineWidth(0)
        self.frame_6.setObjectName("frame_6")
        self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25.setGeometry(QtCore.QRect(40, 395, 30, 30))
        self.label_25.setText("")
        self.label_25.setPixmap(QtGui.QPixmap("icon/all.png"))
        self.label_25.setAlignment(QtCore.Qt.AlignCenter)
        self.label_25.setObjectName("label_25")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(90, 390, 221, 31))
        self.comboBox.setStyleSheet("\n"
                                    "QComboBox {\n"
                                    "    background-color: rgb(98, 105, 121);\n"
                                    "    color: rgb(151, 155, 158);\n"
                                    "    font-size: 14px; /* 设置字体大小为12像素 */\n"
                                    "}\n"
                                    "")  # 设置组合框的对象名称
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(110, 450, 141, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setStyleSheet("background-color: rgb(48,117,152);\n"
                                            "\n"
                                            "border-radius: 15px;\n"
                                            "\n"
                                            "color: rgb(255, 255, 255);")
        self.pushButton_start.setObjectName("pushButton_start")
        self.label_xmin_v = QtWidgets.QLabel(self.centralwidget)
        self.label_xmin_v.setGeometry(QtCore.QRect(110, 780, 70, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_xmin_v.setFont(font)
        self.label_xmin_v.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_xmin_v.setObjectName("label_xmin_v")
        self.label_xmax_v = QtWidgets.QLabel(self.centralwidget)
        self.label_xmax_v.setGeometry(QtCore.QRect(110, 830, 70, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_xmax_v.setFont(font)
        self.label_xmax_v.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_xmax_v.setObjectName("label_xmax_v")
        self.label_ymin_v = QtWidgets.QLabel(self.centralwidget)
        self.label_ymin_v.setGeometry(QtCore.QRect(270, 780, 70, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_ymin_v.setFont(font)
        self.label_ymin_v.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_ymin_v.setObjectName("label_ymin_v")
        self.label_ymax_v = QtWidgets.QLabel(self.centralwidget)
        self.label_ymax_v.setGeometry(QtCore.QRect(270, 830, 70, 35))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.label_ymax_v.setFont(font)
        self.label_ymax_v.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_ymax_v.setObjectName("label_ymax_v")
        self.label_score = QtWidgets.QLabel(self.centralwidget)
        self.label_score.setGeometry(QtCore.QRect(150, 610, 171, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_score.setFont(font)
        self.label_score.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_score.setText("")
        self.label_score.setAlignment(QtCore.Qt.AlignCenter)
        self.label_score.setObjectName("label_score")
        self.label_classes = QtWidgets.QLabel(self.centralwidget)
        self.label_classes.setGeometry(QtCore.QRect(800, 690, 41, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_classes.setFont(font)
        self.label_classes.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_classes.setText("")
        self.label_classes.setObjectName("label_classes")
        self.label_img_path = QtWidgets.QLabel(self.centralwidget)
        self.label_img_path.setGeometry(QtCore.QRect(90, 170, 221, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_img_path.setFont(font)
        self.label_img_path.setToolTipDuration(-1)
        self.label_img_path.setStyleSheet("background-color: rgb(98, 105, 121);\n"
                                          "\n"  # 栏目条
                                          "border-radius: 7px;\n"
                                          "\n"
                                          "color: rgb(151, 155, 158);")
        self.label_img_path.setTextFormat(QtCore.Qt.AutoText)
        self.label_img_path.setObjectName("label_img_path")
        self.pushButton_img = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_img.setGeometry(QtCore.QRect(30, 160, 45, 45))
        self.pushButton_img.setStyleSheet("QPushButton {\n"
                                          "    background-color: transparent;\n"
                                          "    border-radius: 10px; /* 设置圆角半径为10像素 */\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: rgb(98, 105, 121);\n"
                                          "}")
        self.pushButton_img.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/dirs.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_img.setIcon(icon)
        self.pushButton_img.setIconSize(QtCore.QSize(40, 27))
        self.pushButton_img.setObjectName("pushButton_img")
        self.pushButton_dir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_dir.setGeometry(QtCore.QRect(30, 214, 45, 45))
        self.pushButton_dir.setStyleSheet("QPushButton {\n"
                                          "    background-color: transparent;\n"
                                          "    border-radius: 10px; /* 设置圆角半径为10像素 */\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: rgb(98, 105, 121);\n"
                                          "}")
        self.pushButton_dir.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/dir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_dir.setIcon(icon1)
        self.pushButton_dir.setIconSize(QtCore.QSize(40, 27))
        self.pushButton_dir.setObjectName("pushButton_dir")
        self.label_dir_path = QtWidgets.QLabel(self.centralwidget)
        self.label_dir_path.setGeometry(QtCore.QRect(90, 222, 221, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_dir_path.setFont(font)
        self.label_dir_path.setToolTipDuration(-1)
        self.label_dir_path.setStyleSheet("background-color: rgb(98, 105, 121);\n"
                                          "\n"
                                          "border-radius: 7px;\n"
                                          "\n"
                                          "color: rgb(151, 155, 158);\n"
                                          "\n"
                                          "QLabel {\n"
                                          "    padding-left: 10px; /* 设置左边距为10像素 */\n"
                                          "}")
        self.label_dir_path.setTextFormat(QtCore.Qt.AutoText)
        self.label_dir_path.setObjectName("label_dir_path")
        self.pushButton_video = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_video.setGeometry(QtCore.QRect(30, 270, 45, 45))
        self.pushButton_video.setStyleSheet("QPushButton {\n"
                                            "    background-color: transparent;\n"
                                            "    border-radius: 10px; /* 设置圆角半径为10像素 */\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover {\n"
                                            "    background-color: rgb(98, 105, 121);\n"
                                            "}")
        self.pushButton_video.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/Video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_video.setIcon(icon2)
        self.pushButton_video.setIconSize(QtCore.QSize(40, 27))
        self.pushButton_video.setObjectName("pushButton_video")
        self.label_video_path = QtWidgets.QLabel(self.centralwidget)
        self.label_video_path.setGeometry(QtCore.QRect(90, 277, 221, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_video_path.setFont(font)
        self.label_video_path.setToolTipDuration(-1)
        self.label_video_path.setStyleSheet("background-color: rgb(98, 105, 121);\n"
                                            "\n"
                                            "border-radius: 7px;\n"
                                            "\n"
                                            "color: rgb(151, 155, 158);\n"
                                            "\n"
                                            "QLabel {\n"
                                            "    padding-left: 10px; /* 设置左边距为10像素 */\n"
                                            "}")
        self.label_video_path.setTextFormat(QtCore.Qt.AutoText)
        self.label_video_path.setObjectName("label_video_path")
        self.pushButton_export = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_export.setGeometry(QtCore.QRect(110, 510, 141, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_export.setFont(font)
        self.pushButton_export.setStyleSheet("background-color: rgb(48,117,152);\n"
                                             "\n"
                                             "border-radius: 15px;\n"
                                             "\n"
                                             "color: rgb(255, 255, 255);")
        self.pushButton_export.setObjectName("pushButton_export")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(40, 675, 30, 30))
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap("icon/classify.png"))
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(80, 675, 111, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_7.setObjectName("label_7")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(79, 605, 111, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_6.setObjectName("label_6")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(40, 610, 29, 34))
        self.label_14.setText("")
        self.label_14.setPixmap(QtGui.QPixmap("icon/Cofidence_level.png"))
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.tableWidget_info = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_info.setGeometry(QtCore.QRect(350, 670, 891, 211))
        font = QtGui.QFont()
        font.setFamily("黑体")
        self.tableWidget_info.setFont(font)
        self.tableWidget_info.setStyleSheet("")
        self.tableWidget_info.setLineWidth(0)
        self.tableWidget_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget_info.setAutoScroll(False)
        self.tableWidget_info.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_info.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_info.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableWidget_info.setShowGrid(True)
        self.tableWidget_info.setGridStyle(QtCore.Qt.CustomDashLine)
        self.tableWidget_info.setWordWrap(True)
        self.tableWidget_info.setCornerButtonEnabled(True)
        self.tableWidget_info.setRowCount(6)
        self.tableWidget_info.setColumnCount(8)  ##
        self.tableWidget_info.setObjectName("tableWidget_info")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(6, item)
        ##
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_info.setHorizontalHeaderItem(7, item)
        ##
        self.tableWidget_info.horizontalHeader().setVisible(True)
        self.tableWidget_info.horizontalHeader().setCascadingSectionResizes(False)  # 关闭水平标题的级联功能
        self.tableWidget_info.horizontalHeader().setDefaultSectionSize(111)  # 128
        self.tableWidget_info.horizontalHeader().setMinimumSectionSize(30)
        self.tableWidget_info.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_info.verticalHeader().setVisible(False)
        self.tableWidget_info.verticalHeader().setCascadingSectionResizes(False)
        self.label_class = QtWidgets.QLabel(self.centralwidget)
        self.label_class.setGeometry(QtCore.QRect(150, 675, 171, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_class.setFont(font)
        self.label_class.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_class.setText("")
        self.label_class.setAlignment(QtCore.Qt.AlignCenter)
        self.label_class.setObjectName("label_class")
        self.label_control = QtWidgets.QLabel(self.centralwidget)
        self.label_control.setGeometry(QtCore.QRect(17, 150, 321, 731))
        self.label_control.setStyleSheet("background-color: rgba(48, 52, 152, 70);\n"
                                         "border-radius: 15px;\n"
                                         "")
        self.label_control.setText("")
        self.label_control.setObjectName("label_control")
        self.pushButton_camera = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_camera.setGeometry(QtCore.QRect(30, 320, 45, 45))
        self.pushButton_camera.setStyleSheet("QPushButton {\n"
                                             "    background-color: transparent;\n"
                                             "    border-radius: 10px; /* 设置圆角半径为10像素 */\n"
                                             "}\n"
                                             "\n"
                                             "QPushButton:hover {\n"
                                             "    background-color: rgb(98, 105, 121);\n"
                                             "}")
        self.pushButton_camera.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/Camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_camera.setIcon(icon3)
        self.pushButton_camera.setIconSize(QtCore.QSize(40, 27))
        self.pushButton_camera.setObjectName("pushButton_camera")
        self.label_camera_path = QtWidgets.QLabel(self.centralwidget)
        self.label_camera_path.setGeometry(QtCore.QRect(90, 330, 221, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_camera_path.setFont(font)
        self.label_camera_path.setToolTipDuration(-1)
        self.label_camera_path.setStyleSheet("background-color: rgb(98, 105, 121);\n"
                                             "\n"
                                             "border-radius: 7px;\n"
                                             "\n"
                                             "color: rgb(151, 155, 158);\n"
                                             "\n"
                                             "QLabel {\n"
                                             "    padding-left: 10px; /* 设置左边距为10像素 */\n"
                                             "}")
        self.label_camera_path.setTextFormat(QtCore.Qt.AutoText)
        self.label_camera_path.setObjectName("label_camera_path")

        self.pushButton_csv = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_csv.setGeometry(QtCore.QRect(30, 370, 45, 45))
        self.pushButton_csv.setStyleSheet("QPushButton {\n"
                                          "    background-color: transparent;\n"
                                          "    border-radius: 10px; /* 设置圆角半径为10像素 */\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:hover {\n"
                                          "    background-color: rgb(98, 105, 121);\n"
                                          "}")
        self.pushButton_csv.setText("CSV")
        self.pushButton_csv.setObjectName("pushButton_csv")
        self.label_csv_path = QtWidgets.QLabel(self.centralwidget)
        self.label_csv_path.setGeometry(QtCore.QRect(90, 377, 221, 30))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_csv_path.setFont(font)
        self.label_csv_path.setToolTipDuration(-1)
        self.label_csv_path.setStyleSheet(
            "background-color: rgb(98, 105, 121);\n\nborder-radius: 7px;\n\ncolor: rgb(151, 155, 158);\n\nQLabel {\n    padding-left: 10px; /* 设置左边距为10像素 */\n}")
        self.label_csv_path.setTextFormat(QtCore.Qt.AutoText)
        self.label_csv_path.setObjectName("label_csv_path")

        self.label_info = QtWidgets.QLabel(self.centralwidget)
        self.label_info.setGeometry(QtCore.QRect(140, 117, 951, 21))
        self.label_info.setScaledContents(True)
        self.label_info.setAlignment(QtCore.Qt.AlignCenter)
        self.label_info.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextEditable | QtCore.Qt.TextEditorInteraction | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.label_info.setObjectName("label_info")
        self.label_info.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_control.raise_()
        self.label_title.raise_()
        self.frame.raise_()
        self.label_img.raise_()
        self.label_17.raise_()
        self.label_9.raise_()
        self.label_xmin.raise_()
        self.label_19.raise_()
        self.label_20.raise_()
        self.label_21.raise_()
        self.label_23.raise_()
        self.label_24.raise_()
        self.frame_3.raise_()
        self.frame_6.raise_()
        self.label_25.raise_()
        self.comboBox.raise_()
        self.pushButton_start.raise_()
        self.label_xmin_v.raise_()
        self.label_xmax_v.raise_()
        self.label_ymin_v.raise_()
        self.label_ymax_v.raise_()
        self.label_score.raise_()
        self.label_classes.raise_()
        self.label_img_path.raise_()
        self.pushButton_img.raise_()
        self.pushButton_dir.raise_()
        self.label_dir_path.raise_()
        self.pushButton_video.raise_()
        self.label_video_path.raise_()
        self.pushButton_export.raise_()
        self.label_15.raise_()
        self.label_7.raise_()
        self.label_6.raise_()
        self.label_14.raise_()
        self.tableWidget_info.raise_()
        self.label_class.raise_()
        self.pushButton_camera.raise_()
        self.label_camera_path.raise_()
        self.pushButton_csv.raise_()
        self.label_csv_path.raise_()
        self.label_info.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "检测系统"))
        MainWindow.setProperty("setWindowFlags", _translate("MainWindow", "QtCore.Qt.FramelessWindowHint"))
        MainWindow.setProperty("setAttribute", _translate("MainWindow", "QtCore.Qt.WA_TranslucentBackground"))
        self.pushButton_start.setText(_translate("MainWindow", "运行 >"))
        self.label_title.setText(_translate("MainWindow", "检测系统"))  # 标题文本
        self.label_9.setText(_translate("MainWindow", "位置:"))
        self.label_xmin.setText(_translate("MainWindow", "速度X:"))
        self.label_19.setText(_translate("MainWindow", "速度Y:"))
        self.label_20.setText(_translate("MainWindow", "位移X:"))
        self.label_21.setText(_translate("MainWindow", "位移Y:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "所有目标"))
        self.pushButton_start.setText(_translate("MainWindow", "运行 >"))
        self.label_xmin_v.setText(_translate("MainWindow", "0"))
        self.label_xmax_v.setText(_translate("MainWindow", "0"))
        self.label_ymin_v.setText(_translate("MainWindow", "0"))
        self.label_ymax_v.setText(_translate("MainWindow", "0"))
        self.label_img_path.setText(_translate("MainWindow", " 图片"))
        self.label_dir_path.setText(_translate("MainWindow", " 文件夹"))
        self.label_video_path.setText(_translate("MainWindow", " 视频"))
        self.pushButton_export.setText(_translate("MainWindow", "导出 >"))
        self.label_7.setText(_translate("MainWindow", "类别:"))
        self.label_6.setText(_translate("MainWindow", "置信度:"))
        self.tableWidget_info.setSortingEnabled(False)
        self.tableWidget_info.setProperty("sectionResizeMode",
                                          _translate("MainWindow", "QHeaderView::ResizeToContents"))
        item = self.tableWidget_info.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "编号"))
        item = self.tableWidget_info.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "文件名"))
        item = self.tableWidget_info.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "输入时间"))
        item = self.tableWidget_info.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "结果"))
        item = self.tableWidget_info.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "目标数量"))
        item = self.tableWidget_info.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "耗时"))
        item = self.tableWidget_info.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "保存路径"))
        ##
        item = self.tableWidget_info.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "置信度"))
        ##
        self.label_camera_path.setText(_translate("MainWindow", " 摄像头"))
        self.label_csv_path.setText(_translate("MainWindow", " CSV"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())