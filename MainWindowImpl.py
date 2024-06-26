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
import azure.cognitiveservices.speech as speechsdk
import MainWindow
import PlayWidget
import SetWidget


class MainWindowImpl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.read_settings()
        self.init_speech_config()

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

        self._init_play_button()

    def _init_play_button(self):
        self.playwidget.pushButton_play.clicked.connect(self.on_play_clicked)

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

        # read voice_speed setting
        voice_speed = settings.value("voice_speed", "1")
        self.setwidget.doubleSpinBox_voice_speed.setValue(float(voice_speed))

    def write_settings(self):

        settings = QSettings("xujialiu", "text-to-speech")

        # save speech_key setting
        settings.setValue("speech_key", self.setwidget.lineEdit_speech_key.text())

        # save speech_region setting
        settings.setValue("speech_region", self.setwidget.lineEdit_speech_region.text())

        # save voice_speed setting
        settings.setValue(
            "voice_speed", self.setwidget.doubleSpinBox_voice_speed.text()
        )

    def init_speech_config(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def on_play_clicked(self):
        self.text = self.playwidget.textEdit_text.toPlainText()
        self.speed = self.setwidget.doubleSpinBox_voice_speed.text()
        self.ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">'
            f'<voice name="en-US-AvaNeural">'
            f'<prosody rate="{self.speed}">'
            f"{self.text}"
            "</prosody>"
            "</voice>\n"
            "</speak>\n"
        )

        self.synthesizer.speak_ssml_async(self.ssml).get()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindowImpl()
    window.show()
    sys.exit(app.exec())
