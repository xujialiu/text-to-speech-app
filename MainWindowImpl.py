# -*- coding: utf-8 -*-

import json
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
        self._init_app()
        self._init_mainwindow()
        self._init_playwidget()
        self._init_setwidget()
        self._init_language_type()

    def _load_meta_json(self):
        file_path = "meta.json"
        with open(file_path) as file:
            self.meta_data = json.load(file)

    def _init_language_type(self):
        self._load_meta_json()

        for item in self.meta_data["voice"]:
            self.setwidget.comboBox_language_type.addItem(
                item["name"], (item["region"], item["voices"])
            )

        self.setwidget.comboBox_language_type.setCurrentIndex(-1)
        self.setwidget.comboBox_language_type.currentIndexChanged.connect(
            self.on_language_type_selected
        )

    def on_language_type_selected(self, index):
        self.setwidget.comboBox_voice_type.clear()
        region, voices = self.setwidget.comboBox_language_type.itemData(index)
        self.setwidget.comboBox_voice_type.addItems(voices)

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
        # save settings before closed
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

        # read language_type setting
        language_type = settings.value("language_type", "-1")
        self.setwidget.comboBox_language_type.setCurrentIndex(int(language_type))

        # read voice_type setting
        voice_type = settings.value("voice_type", "-1")
        self.setwidget.comboBox_voice_type.setCurrentIndex(int(voice_type))

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

        # save language_type setting
        settings.setValue(
            "language_type", self.setwidget.comboBox_language_type.currentIndex()
        )

        # save voice_type setting
        settings.setValue(
            "voice_type", self.setwidget.comboBox_voice_type.currentIndex()
        )

    def init_speech_config(self):
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def on_play_clicked(self):
        self.text = self.playwidget.textEdit_text.toPlainText()
        self.speed = self.setwidget.doubleSpinBox_voice_speed.text()
        self.lang = self.setwidget.comboBox_language_type.currentText()

        self.voice_type = self.setwidget.comboBox_voice_type.currentText()
        self.voice = self.voice_type.split()[0]

        self.lang, _ = self.setwidget.comboBox_language_type.currentData()

        self.ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.lang}">'
            f'<voice name="{self.lang}-{self.voice}">'
            f'<prosody rate="{self.speed}">'
            f"{self.text}"
            "</prosody>"
            "</voice>"
            "</speak>"
        )
        self.synthesizer.speak_ssml_async(self.ssml).get()

    def _init_app(self):
        app = QApplication.instance()
        app.setStyle("fusion")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindowImpl()
    window.show()
    sys.exit(app.exec())
