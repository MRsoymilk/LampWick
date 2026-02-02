# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Monitor.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QGridLayout,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QSpinBox, QToolButton, QVBoxLayout, QWidget)

class Ui_Monitor(object):
    def setupUi(self, Monitor):
        if not Monitor.objectName():
            Monitor.setObjectName(u"Monitor")
        Monitor.resize(548, 464)
        self.gridLayout = QGridLayout(Monitor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.labelVideo = QLabel(Monitor)
        self.labelVideo.setObjectName(u"labelVideo")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVideo.sizePolicy().hasHeightForWidth())
        self.labelVideo.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.labelVideo, 0, 0, 2, 2)

        self.hLayCamera = QHBoxLayout()
        self.hLayCamera.setObjectName(u"hLayCamera")
        self.labelCamera = QLabel(Monitor)
        self.labelCamera.setObjectName(u"labelCamera")

        self.hLayCamera.addWidget(self.labelCamera)

        self.comboBoxCamera = QComboBox(Monitor)
        self.comboBoxCamera.setObjectName(u"comboBoxCamera")

        self.hLayCamera.addWidget(self.comboBoxCamera)


        self.gridLayout.addLayout(self.hLayCamera, 4, 0, 1, 2)

        self.hLayOverlayOperate = QHBoxLayout()
        self.hLayOverlayOperate.setObjectName(u"hLayOverlayOperate")
        self.tBtnDraw4Line = QToolButton(Monitor)
        self.tBtnDraw4Line.setObjectName(u"tBtnDraw4Line")

        self.hLayOverlayOperate.addWidget(self.tBtnDraw4Line)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hLayOverlayOperate.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.hLayOverlayOperate, 2, 0, 1, 2)

        self.hLayOperation = QHBoxLayout()
        self.hLayOperation.setObjectName(u"hLayOperation")
        self.hLayCameraOperate = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hLayOperation.addItem(self.hLayCameraOperate)

        self.tBtnRecord = QToolButton(Monitor)
        self.tBtnRecord.setObjectName(u"tBtnRecord")

        self.hLayOperation.addWidget(self.tBtnRecord)

        self.vLayOffsetH = QVBoxLayout()
        self.vLayOffsetH.setObjectName(u"vLayOffsetH")
        self.tBtnOffsetH = QToolButton(Monitor)
        self.tBtnOffsetH.setObjectName(u"tBtnOffsetH")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tBtnOffsetH.sizePolicy().hasHeightForWidth())
        self.tBtnOffsetH.setSizePolicy(sizePolicy1)

        self.vLayOffsetH.addWidget(self.tBtnOffsetH)

        self.spinBoxOffsetH = QSpinBox(Monitor)
        self.spinBoxOffsetH.setObjectName(u"spinBoxOffsetH")
        self.spinBoxOffsetH.setMinimum(-999)
        self.spinBoxOffsetH.setMaximum(999)

        self.vLayOffsetH.addWidget(self.spinBoxOffsetH)


        self.hLayOperation.addLayout(self.vLayOffsetH)

        self.vLayOffsetV = QVBoxLayout()
        self.vLayOffsetV.setObjectName(u"vLayOffsetV")
        self.tBtnOffsetV = QToolButton(Monitor)
        self.tBtnOffsetV.setObjectName(u"tBtnOffsetV")
        sizePolicy1.setHeightForWidth(self.tBtnOffsetV.sizePolicy().hasHeightForWidth())
        self.tBtnOffsetV.setSizePolicy(sizePolicy1)

        self.vLayOffsetV.addWidget(self.tBtnOffsetV)

        self.spinBoxOffsetV = QSpinBox(Monitor)
        self.spinBoxOffsetV.setObjectName(u"spinBoxOffsetV")
        self.spinBoxOffsetV.setMinimum(-999)
        self.spinBoxOffsetV.setMaximum(999)

        self.vLayOffsetV.addWidget(self.spinBoxOffsetV)


        self.hLayOperation.addLayout(self.vLayOffsetV)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tBtnRotate = QToolButton(Monitor)
        self.tBtnRotate.setObjectName(u"tBtnRotate")
        sizePolicy1.setHeightForWidth(self.tBtnRotate.sizePolicy().hasHeightForWidth())
        self.tBtnRotate.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.tBtnRotate)

        self.doubleSpinBoxRotate = QDoubleSpinBox(Monitor)
        self.doubleSpinBoxRotate.setObjectName(u"doubleSpinBoxRotate")
        self.doubleSpinBoxRotate.setMinimum(-360.000000000000000)
        self.doubleSpinBoxRotate.setMaximum(360.000000000000000)

        self.verticalLayout.addWidget(self.doubleSpinBoxRotate)


        self.hLayOperation.addLayout(self.verticalLayout)


        self.gridLayout.addLayout(self.hLayOperation, 3, 0, 1, 2)

        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 7)
        self.gridLayout.setColumnStretch(1, 3)

        self.retranslateUi(Monitor)

        QMetaObject.connectSlotsByName(Monitor)
    # setupUi

    def retranslateUi(self, Monitor):
        Monitor.setWindowTitle(QCoreApplication.translate("Monitor", u"Form", None))
        self.labelVideo.setText(QCoreApplication.translate("Monitor", u"video", None))
        self.labelCamera.setText(QCoreApplication.translate("Monitor", u"camera", None))
        self.tBtnDraw4Line.setText(QCoreApplication.translate("Monitor", u"draw 4 line", None))
        self.tBtnRecord.setText(QCoreApplication.translate("Monitor", u"record", None))
        self.tBtnOffsetH.setText(QCoreApplication.translate("Monitor", u"offset h", None))
        self.tBtnOffsetV.setText(QCoreApplication.translate("Monitor", u"offset v", None))
        self.tBtnRotate.setText(QCoreApplication.translate("Monitor", u"rotate", None))
    # retranslateUi

