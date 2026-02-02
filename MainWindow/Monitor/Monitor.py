from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import (
    QImage,
    QPixmap,
    QPainter,
    QPen,
    QFont,
    QColor,
    QTransform
)

import os
import configparser
import cv2
import numpy as np

from MainWindow.Monitor.ui_Monitor import Ui_Monitor
from MainWindow.Monitor.HandleOverlay import HandleOverlay

class Monitor(QWidget, Ui_Monitor):
    CONFIG_PATH = "config/camera.ini"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.labelVideo.setMinimumSize(240, 240)
        self.labelVideo.setAlignment(Qt.AlignCenter)

        self.camera_indices = []

        self.scan_cameras()
        self.comboBoxCamera.currentIndexChanged.connect(
            self.on_camera_changed
        )

        self.tBtnDraw4Line.setCheckable(True)
        self.tBtnDraw4Line.clicked.connect(self.on_click_tBtnDraw4Line)

        self.enableDraw4Line = False

        self.overlay = HandleOverlay(self.labelVideo)
        self.overlay.setGeometry(self.labelVideo.rect())
        self.overlay.show()

        self.video_writer = None
        self.output_video_path = "full_monitor.mp4"
        self.fps = 30

        self.tBtnRecord.setCheckable(True)
        self.tBtnRecord.clicked.connect(self.on_click_tBtnRecord)
        self.record = False

        self.tBtnOffsetH.setCheckable(True)
        self.tBtnOffsetH.clicked.connect(self.on_click_tBtnOffsetH)
        self.offset_h = 0
        self.enableOffsetH = False
        self.spinBoxOffsetH.valueChanged.connect(self.on_spinBoxOffsetHChanged)

        self.tBtnOffsetV.setCheckable(True)
        self.tBtnOffsetV.clicked.connect(self.on_click_tBtnOffsetV)
        self.offset_v = 0
        self.enableOffsetV = False
        self.spinBoxOffsetV.valueChanged.connect(self.on_spinBoxOffsetVChanged)

        self.tBtnRotate.setCheckable(True)
        self.tBtnRotate.clicked.connect(self.on_click_tBtnRotate)
        self.rotate = 0
        self.enableRotate = False
        self.doubleSpinBoxRotate.valueChanged.connect(self.on_doubleSpinBoxRotateChanged)

        self._load_from_config()

    def _load_from_config(self):
        if not os.path.exists(self.CONFIG_PATH):
            return

        config = configparser.ConfigParser()
        try:
            config.read(self.CONFIG_PATH)
            if 'Camera' in config:
                section = config['Camera']
                self.offset_h = int(section.get('offset_h',    '0'))
                self.offset_v = int(section.get('offset_v',    '0'))
                self.rotate = float(section.get('rotate',    '0'))
                self.spinBoxOffsetH.setValue(self.offset_h)
                self.spinBoxOffsetV.setValue(self.offset_v)
                self.doubleSpinBoxRotate.setValue(self.rotate)
        except Exception as e:
            print(f"加载 {self.CONFIG_PATH} 失败: {e}，使用默认值")

    def save_to_config(self):
        os.makedirs(os.path.dirname(self.CONFIG_PATH), exist_ok=True)
        config = configparser.ConfigParser()
        config['Camera'] = {
            'offset_h':    f"{self.offset_h}",
            'offset_v': f"{self.offset_v}",
            'rotate':   f"{self.rotate}",
        }
        try:
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                config.write(f)
            print(f"已保存相机设置到 {self.CONFIG_PATH}")
        except Exception as e:
            print(f"保存 {self.CONFIG_PATH} 失败: {e}")

    def on_spinBoxOffsetHChanged(self, value):
        if self.enableOffsetH:
            self.offset_h = value
            print("offset h: ", value)
            self.save_to_config()

    def on_spinBoxOffsetVChanged(self, value):
        if self.enableOffsetV:
            self.offset_v = value
            print("offset v: ", value)
            self.save_to_config()

    def on_doubleSpinBoxRotateChanged(self, value):
        if self.enableRotate:
            self.rotate = value
            print("rotate: ", value)
            self.save_to_config()

    def on_click_tBtnOffsetH(self):
        self.enableOffsetH = not self.enableOffsetH

    def on_click_tBtnOffsetV(self):
        self.enableOffsetV = not self.enableOffsetV

    def on_click_tBtnRotate(self):
        self.enableRotate = not self.enableRotate

    def on_click_tBtnRecord(self):
        self.record = not self.record

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.setGeometry(self.labelVideo.rect())

    def on_click_tBtnDraw4Line(self):
        self.enableDraw4Line = not self.enableDraw4Line
        self.overlay.set_draw_mode(self.enableDraw4Line)

    def on_camera_changed(self, index):
        if index < 0:
            return
        self.start_camera()

    def scan_cameras(self, max_test=5):
        """扫描可用摄像头"""
        self.comboBoxCamera.clear()
        self.camera_indices.clear()

        for i in range(max_test):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                # 成功打开摄像头
                self.camera_indices.append(i)
                self.comboBoxCamera.addItem(f"Camera {i}", i)
                cap.release()  # 释放立即关闭，避免占用
            else:
                cap.release()

    def start_camera(self):
        self.stop_camera()

        # 获取 comboBox 当前选中的摄像头 index
        index = self.comboBoxCamera.currentIndex()
        if index < 0:
            print("❌ No camera selected")
            return

        cam_index = self.comboBoxCamera.itemData(index)
        self.cap = cv2.VideoCapture(cam_index)
        if not self.cap.isOpened():
            print("❌ Failed to open camera:", cam_index)
            self.cap = None
            return

        print("✅ Camera opened:", cam_index)
        self.timer.start(30)  # ~30 FPS


    def stop_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
            self.cap = None

    def update_frame(self):
        if not self.cap:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        # BGR -> RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape

        # ===============================
        # 镜头平移 + 补黑
        # ===============================
        offset_h = int(self.offset_h) if self.enableOffsetH else 0
        offset_v = int(self.offset_v) if self.enableOffsetV else 0

        if offset_h != 0 or offset_v != 0:
            # 黑色背景
            shifted = np.zeros_like(frame_rgb)

            # 源图裁剪区域
            src_x1 = max(0, -offset_h)
            src_y1 = max(0, -offset_v)
            src_x2 = min(w, w - offset_h)
            src_y2 = min(h, h - offset_v)

            # 目标图粘贴区域
            dst_x1 = max(0, offset_h)
            dst_y1 = max(0, offset_v)
            dst_x2 = dst_x1 + (src_x2 - src_x1)
            dst_y2 = dst_y1 + (src_y2 - src_y1)

            if src_x1 < src_x2 and src_y1 < src_y2:
                shifted[dst_y1:dst_y2, dst_x1:dst_x2] = \
                    frame_rgb[src_y1:src_y2, src_x1:src_x2]

            frame_rgb = shifted
        # ===============================

        # 转 QImage
        qimg = QImage(
            frame_rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(qimg)

        # 旋转
        if self.enableRotate:
            transform = QTransform()
            transform.rotate(self.rotate)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)

        # 显示
        self.labelVideo.setPixmap(
            pixmap.scaled(
                self.labelVideo.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        if self.record:
            # ===== 抓取整个 Monitor 界面 =====
            full_pixmap = self.grab()
            img = full_pixmap.toImage().convertToFormat(QImage.Format_RGB888)

            w, h = img.width(), img.height()
            bpl = img.bytesPerLine()

            ptr = img.bits()
            arr = np.array(ptr, dtype=np.uint8).reshape(h, bpl)

            frame_rgb = arr[:, :w*3].reshape(h, w, 3)

            frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

            # ===== 初始化 VideoWriter =====
            if self.video_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                self.video_writer = cv2.VideoWriter(self.output_video_path, fourcc, self.fps, (w, h))

            # ===== 写入视频 =====
            self.video_writer.write(frame_bgr)

    def closeEvent(self, event):
        self.stop_camera()
        if self.cap:
            self.cap.release()
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        event.accept()

    def close_video(self):
        self.stop_camera()

    def open_video_file(self, video_path: str):
        self.stop_camera()

        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            print("❌ Failed to open video:", video_path)
            self.cap = None
            return

        self.timer.start(30)
