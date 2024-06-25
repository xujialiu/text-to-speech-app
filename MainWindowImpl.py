# -*- coding: utf-8 -*-

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
)
from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSettings,
    QSize,
    QTime,
    QUrl,
    Qt,
)

import MainWindow
import PlayWidget
import SetWidget


class MainWindowImpl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.read_settings()

    def init_ui(self):
        self._init_mainwindow()
        self._init_playwidget()
        self._init_setwidget()

    def _init_mainwindow(self):
        self.mainwindow = MainWindow.Ui_MainWindow()
        self.mainwindow.setupUi(self)

    def _init_playwidget(self):
        self.playwidget = PlayWidget.Ui_Form()
        self.playwidget.setupUi(self.mainwindow.tab_play)

    def _init_setwidget(self):
        self.setwidget = SetWidget.Ui_Form()
        self.setwidget.setupUi(self.mainwindow.tab_setting)

    def closeEvent(self, event):
        # 在关闭窗口时保存QLineEdit的内容
        self.write_settings()
        event.accept()

    def read_settings(self):
        settings = QSettings("xujialiu", "text-to-speech")

        # read speech_key setting
        self.speech_key = settings.value("speech_key", "")
        self.setwidget.lineEdit_speech_key.setText(self.speech_key)

        # read speech_region setting
        self.speech_region = settings.value("speech_region", "")
        self.setwidget.lineEdit_speech_region.setText(self.speech_region)

    def write_settings(self):

        settings = QSettings("xujialiu", "text-to-speech")

        # save speech_key setting
        settings.setValue("speech_key", self.setwidget.lineEdit_speech_key.text())

        # save speech_region setting
        settings.setValue("speech_region", self.setwidget.lineEdit_speech_region.text())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindowImpl()
    window.show()
    sys.exit(app.exec())
