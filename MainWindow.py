# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(626, 419)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget_debug = QTabWidget(Form)
        self.tabWidget_debug.setObjectName(u"tabWidget_debug")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tabWidget_debug.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget_debug.addTab(self.tab_2, "")
        self.tab_debug = QWidget()
        self.tab_debug.setObjectName(u"tab_debug")
        self.verticalLayout_2 = QVBoxLayout(self.tab_debug)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_debug = QLineEdit(self.tab_debug)
        self.lineEdit_debug.setObjectName(u"lineEdit_debug")

        self.horizontalLayout.addWidget(self.lineEdit_debug)

        self.pushButton_debug = QPushButton(self.tab_debug)
        self.pushButton_debug.setObjectName(u"pushButton_debug")

        self.horizontalLayout.addWidget(self.pushButton_debug)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tabWidget_debug.addTab(self.tab_debug, "")

        self.verticalLayout.addWidget(self.tabWidget_debug)


        self.retranslateUi(Form)

        self.tabWidget_debug.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidget_debug.setTabText(self.tabWidget_debug.indexOf(self.tab), QCoreApplication.translate("Form", u"Play", None))
        self.tabWidget_debug.setTabText(self.tabWidget_debug.indexOf(self.tab_2), QCoreApplication.translate("Form", u"Setting", None))
        self.pushButton_debug.setText(QCoreApplication.translate("Form", u"Execute", None))
        self.tabWidget_debug.setTabText(self.tabWidget_debug.indexOf(self.tab_debug), QCoreApplication.translate("Form", u"Debug", None))
    # retranslateUi

