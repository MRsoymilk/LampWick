# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QSizePolicy,
    QSpacerItem, QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(884, 575)
        self.gridLayout = QGridLayout(MainWindow)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.tBtnFromCamera = QToolButton(MainWindow)
        self.tBtnFromCamera.setObjectName(u"tBtnFromCamera")

        self.horizontalLayout.addWidget(self.tBtnFromCamera)

        self.tBtnFromVideo = QToolButton(MainWindow)
        self.tBtnFromVideo.setObjectName(u"tBtnFromVideo")

        self.horizontalLayout.addWidget(self.tBtnFromVideo)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.gLay = QGridLayout()
        self.gLay.setObjectName(u"gLay")

        self.gridLayout.addLayout(self.gLay, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"DoWater", None))
        self.tBtnFromCamera.setText(QCoreApplication.translate("MainWindow", u"From Camera", None))
        self.tBtnFromVideo.setText(QCoreApplication.translate("MainWindow", u"From Video", None))
    # retranslateUi

