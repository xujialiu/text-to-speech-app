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


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindowImpl()
    window.show()
    sys.exit(app.exec())
