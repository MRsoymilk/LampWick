from PySide6.QtWidgets import QWidget, QFileDialog
from MainWindow.ui_MainWindow import Ui_MainWindow
from MainWindow.Monitor.Monitor import Monitor

class MainWindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tBtnFromCamera.setCheckable(True)
        self.tBtnFromCamera.clicked.connect(self.on_click_tBtnFromCamera)
        self.tBtnFromVideo.setCheckable(True)
        self.tBtnFromVideo.clicked.connect(self.on_click_tBtnFromVideo)

        self.monitor = Monitor()
        self.gLay.addWidget(self.monitor)

    def on_click_tBtnFromCamera(self):
        print("From Camera")
        if self.tBtnFromCamera.isChecked():
            self.monitor.start_camera()
        else:
            self.monitor.close_video()

    def on_click_tBtnFromVideo(self):
        print("From Video")
        if self.tBtnFromVideo.isChecked():
            video_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "choose video file",
                    "",\
                    "Video Files (*.mp4 *.avi *.mkv *.mov);;All Files (*)"
                )

            if not video_path:
                return

            self.monitor.open_video_file(video_path)
        else:
            self.monitor.close_video()


