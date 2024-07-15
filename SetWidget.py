# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetWidget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QKeySequenceEdit, QLabel, QLineEdit,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(854, 685)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        font = QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)

        self.verticalLayout.addWidget(self.label_10)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lineEdit_speech_key = QLineEdit(Form)
        self.lineEdit_speech_key.setObjectName(u"lineEdit_speech_key")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_speech_key.sizePolicy().hasHeightForWidth())
        self.lineEdit_speech_key.setSizePolicy(sizePolicy)
        self.lineEdit_speech_key.setMinimumSize(QSize(300, 0))

        self.horizontalLayout.addWidget(self.lineEdit_speech_key)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.lineEdit_speech_region = QLineEdit(Form)
        self.lineEdit_speech_region.setObjectName(u"lineEdit_speech_region")
        sizePolicy.setHeightForWidth(self.lineEdit_speech_region.sizePolicy().hasHeightForWidth())
        self.lineEdit_speech_region.setSizePolicy(sizePolicy)
        self.lineEdit_speech_region.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_2.addWidget(self.lineEdit_speech_region)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.comboBox_language_type = QComboBox(Form)
        self.comboBox_language_type.setObjectName(u"comboBox_language_type")
        self.comboBox_language_type.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_3.addWidget(self.comboBox_language_type)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.comboBox_voice_type = QComboBox(Form)
        self.comboBox_voice_type.setObjectName(u"comboBox_voice_type")
        self.comboBox_voice_type.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_4.addWidget(self.comboBox_voice_type)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.doubleSpinBox_voice_speed = QDoubleSpinBox(Form)
        self.doubleSpinBox_voice_speed.setObjectName(u"doubleSpinBox_voice_speed")
        self.doubleSpinBox_voice_speed.setDecimals(1)
        self.doubleSpinBox_voice_speed.setSingleStep(0.100000000000000)
        self.doubleSpinBox_voice_speed.setValue(1.000000000000000)

        self.horizontalLayout_5.addWidget(self.doubleSpinBox_voice_speed)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font)

        self.verticalLayout.addWidget(self.label_9)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)

        self.keySequenceEdit_covert = QKeySequenceEdit(Form)
        self.keySequenceEdit_covert.setObjectName(u"keySequenceEdit_covert")
        sizePolicy.setHeightForWidth(self.keySequenceEdit_covert.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit_covert.setSizePolicy(sizePolicy)
        self.keySequenceEdit_covert.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_6.addWidget(self.keySequenceEdit_covert)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_8.addWidget(self.label_8)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)

        self.keySequenceEdit_stop = QKeySequenceEdit(Form)
        self.keySequenceEdit_stop.setObjectName(u"keySequenceEdit_stop")
        sizePolicy.setHeightForWidth(self.keySequenceEdit_stop.sizePolicy().hasHeightForWidth())
        self.keySequenceEdit_stop.setSizePolicy(sizePolicy)
        self.keySequenceEdit_stop.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_8.addWidget(self.keySequenceEdit_stop)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticalSpacer = QSpacerItem(20, 162, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"General:", None))
        self.label.setText(QCoreApplication.translate("Form", u"Speech key", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Speech region", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Language type", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Voice type", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Voice speech", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Global Hotkeys:", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Convert text to speech", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Stop conversion", None))
    # retranslateUi

