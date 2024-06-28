# -*- coding: utf-8 -*-
# TODO:
# [[bug]]: speak_ssml_async存在线程阻塞问题

import json
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
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
    QThread,
    QTime,
    QUrl,
    Qt,
    Signal,
    Slot,
)
import azure.cognitiveservices.speech as speechsdk
import MainWindow
import PlayWidget
import SetWidget
import DebugWidget
from pynput import keyboard

import re


class MainWindowImpl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.convert = 0
        self.play_pause = 0
        self.global_hotkeys_listener = None
        self.dict_fn_hotkey = {
            self.on_play_hotkey_triggered: None,
            self.on_play_pause_hotkey_triggered: None,
            self.on_stop_hotkey_triggered: None,
        }
        self.dict_hotkey_fn = dict()

        self.init_ui()
        self.read_settings()
        self.init_speech_synthesizer()

    def init_ui(self):
        self._init_app()
        self._init_mainwindow()
        self._init_playwidget()
        self._init_setwidget()
        self._init_debugwidget()

        self._init_tray_menu()
        self._init_tray_icon()

        self._init_keysequenceedit()

        self._init_speech_region()
        self._init_speech_key()
        self._init_language_type()
        self._init_voice_type()
        self._init_voice_speech()
        self._init_clipboard()

    def _init_speech_key(self):
        self.setwidget.lineEdit_speech_key.textChanged.connect(
            self.on_speech_key_changed
        )

    def on_speech_key_changed(self, text):
        self.speech_key = text
        self.init_speech_synthesizer()

    def _init_speech_region(self):
        self.setwidget.lineEdit_speech_region.textChanged.connect(
            self.on_speech_region_changed
        )

    def on_speech_region_changed(self, text):
        self.speech_region = text
        self.init_speech_synthesizer()

    def _init_clipboard(self):
        self.clipboard = QApplication.clipboard()

    def _init_keysequenceedit(self):

        self.setwidget.keySequenceEdit_covert.keySequenceChanged.connect(
            self.set_convert_hotkey
        )
        self.setwidget.keySequenceEdit_play_pause.keySequenceChanged.connect(
            self.set_play_pause_hotkey
        )
        self.setwidget.keySequenceEdit_stop.keySequenceChanged.connect(
            self.set_stop_hotkey
        )

    def set_hotkey(self, str_keysequence, on_keysequence_triggered):
        if str_keysequence:
            # 如果global_hotkeys_listener不为None, 先停下
            if self.global_hotkeys_listener:
                self.global_hotkeys_listener.stop()

            # 解析为pynput可以理解的hotkey
            pynput_hotkey = self.parse_hotkey(str_keysequence)

            self.update_dict_fn_hotkey(pynput_hotkey, on_keysequence_triggered)
            self.update_dict_hotkey_fn()

            if self.dict_fn_hotkey:
                self.global_hotkeys_listener = keyboard.GlobalHotKeys(
                    self.dict_hotkey_fn
                )
                self.global_hotkeys_listener.start()

    def set_convert_hotkey(self):
        str_keysequence_convert = self.convert_keysequence_to_string(
            self.setwidget.keySequenceEdit_covert
        )
        self.set_hotkey(str_keysequence_convert, self.on_play_hotkey_triggered)

    def set_play_pause_hotkey(self):
        str_keysequence_play_pause = self.convert_keysequence_to_string(
            self.setwidget.keySequenceEdit_play_pause
        )
        self.set_hotkey(str_keysequence_play_pause, self.on_play_pause_hotkey_triggered)

    def set_stop_hotkey(self):
        str_keysequence_stop = self.convert_keysequence_to_string(
            self.setwidget.keySequenceEdit_stop
        )
        self.set_hotkey(str_keysequence_stop, self.on_stop_hotkey_triggered)

    @staticmethod
    def split_text(text: str):
        text = re.sub(r"\n+", "\n", text)
        list_split_text = re.split(r"(?<=。)|(?<=\.\s)|(?<=\n)", text)
        # if用于去除空字符串
        list_split_text = [
            sentence.strip() for sentence in list_split_text if sentence.strip()
        ]

        return list_split_text

    def on_play_hotkey_triggered(self):
        self.text = self.clipboard.text()
        self.list_split_text = self.split_text(self.text)

        # print(self.list_split_text)

        # 先合成第一句, 第一句需要阻塞进程
        ssml_text0 = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.language_type}">'
            f'<voice name="{self.language_type}-{self.voice}">'
            f'<prosody rate="{self.voice_speed}">'
            f"{self.list_split_text[0]}"
            "</prosody>"
            "</voice>"
            "</speak>"
        )
        

        speech_config_text0 = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

        audio_config_text0 = speechsdk.audio.AudioOutputConfig(filename="test0.mp3")

        synthesizer_text0 = speechsdk.SpeechSynthesizer(
            speech_config=speech_config_text0, audio_config=audio_config_text0
        )
        print(1)
        synthesizer_text0.speak_ssml_async(ssml_text0)
        print(self.list_split_text)
        print(1)
        
        

    def synthesize_other_speech(self):
        """合成第二句往后, 不需要阻塞线程, 这里启动里一个线程运行"""
        for i, text in enumerate(self.list_split_text[1:], 1):

            audio_config = speechsdk.audio.AudioOutputConfig(filename="test{i}.mp3")
            ssml = (
                f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.language_type}">'
                f'<voice name="{self.language_type}-{self.voice}">'
                f'<prosody rate="{self.voice_speed}">'
                f"{self.text}"
                "</prosody>"
                "</voice>"
                "</speak>"
            )

            synthesizer_text0 = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, audio_config=audio_config
            )

            synthesizer_text0.speak_ssml_async(ssml)

    def on_play_pause_hotkey_triggered(self):
        print(2)

    def on_stop_hotkey_triggered(self):
        print(3)

    def update_dict_fn_hotkey(self, pynput_hotkey, fn):
        self.dict_fn_hotkey[fn] = pynput_hotkey

    def update_dict_hotkey_fn(self):
        self.dict_hotkey_fn = dict()
        try:
            for fn, hotkey in self.dict_fn_hotkey.items():
                if hotkey:
                    self.dict_hotkey_fn[hotkey] = fn
        except:
            pass

    @staticmethod
    def convert_keysequence_to_string(keysequenceedit):
        return keysequenceedit.keySequence().toString(QKeySequence.NativeText)

    def parse_hotkey(self, key_sequence):
        key_map = {
            "Ctrl": "<ctrl>",
            "Alt": "<alt>",
            "Shift": "<shift>",
            "Meta": "<cmd>",
        }
        keys = key_sequence.split("+")
        parsed_keys = []
        for key in keys:
            key = key.strip()
            if key in key_map:
                parsed_keys.append(key_map[key])
            else:
                parsed_keys.append(key.lower())
        return "+".join(parsed_keys)

    def _init_debugwidget(self):
        self.debugwidget = DebugWidget.Ui_Form()
        self.debugwidget.setupUi(self.mainwindow.tab_debug)
        self.debugwidget.pushButton_debug.clicked.connect(self.on_debug_clicked)

    def on_debug_clicked(self):
        code = self.debugwidget.textEdit_debug.toPlainText()

        try:
            exec(f"{code}")
        except Exception as e:
            print(e)


    def _init_tray_menu(self):
        self.tray_menu = QMenu()
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.on_close_clicked)
        self.tray_menu.addAction(close_action)

    def _init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))  # 设置系统托盘图标
        self.tray_icon.setToolTip("Azure-Text-To-Speech")

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def on_close_clicked(self):
        """真正的关闭事件"""
        self.tray_icon.hide()
        # save settings before closed
        self.write_settings()
        self.global_hotkeys_listener.stop()
        QApplication.quit()

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

        self.setwidget.comboBox_language_type.currentIndexChanged.connect(
            self.on_language_type_changed
        )

    def on_language_type_changed(self, index):
        self.language_type, _ = self.setwidget.comboBox_language_type.currentData()

    def on_language_type_selected(self, index):
        """当选择了language_type时, 更新combobox_voice_type列表"""
        self.setwidget.comboBox_voice_type.clear()
        region, voices = self.setwidget.comboBox_language_type.itemData(index)
        self.setwidget.comboBox_voice_type.addItems(voices)

    def _init_voice_type(self):
        self.setwidget.comboBox_voice_type.currentTextChanged.connect(
            self.on_voice_type_changed
        )

    def on_voice_type_changed(self, text):
        self.voice_type = text
        self.voice = self.voice_type.split()[0]

    def _init_voice_speech(self):
        self.setwidget.doubleSpinBox_voice_speed.valueChanged.connect(
            self.on_voice_speed_changed
        )

    def on_voice_speed_changed(self, value):
        self.voice_speed = value

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
        """点击主窗口右上角的x的事件, 并非真正的关闭事件"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Azure-Text-To-Speech",
            "The program has been minimized to the system tray.",
            QSystemTrayIcon.Information,
            2000,
        )

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

        # save keySequenceEdit
        # read keySequenceEdit for convert_text_to_speech
        convert_key_sequence = settings.value("convert_text_to_speech", "")
        if convert_key_sequence:
            self.setwidget.keySequenceEdit_covert.setKeySequence(
                QKeySequence(convert_key_sequence)
            )

        # read keySequenceEdit for pause_or_resume_speech
        play_pause_key_sequence = settings.value("pause_or_resume_speech", "")
        if play_pause_key_sequence:
            self.setwidget.keySequenceEdit_play_pause.setKeySequence(
                QKeySequence(play_pause_key_sequence)
            )

        # read keySequenceEdit for stop_conversion
        stop_key_sequence = settings.value("stop_conversion", "")
        if stop_key_sequence:
            self.setwidget.keySequenceEdit_stop.setKeySequence(
                QKeySequence(stop_key_sequence)
            )

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

        # save keySequenceEdit
        settings.setValue(
            "convert_text_to_speech",
            self.setwidget.keySequenceEdit_covert.keySequence(),
        )
        settings.setValue(
            "pause_or_resume_speech",
            self.setwidget.keySequenceEdit_play_pause.keySequence(),
        )
        settings.setValue(
            "stop_conversion", self.setwidget.keySequenceEdit_stop.keySequence()
        )

    def init_speech_synthesizer(self):
        try:
            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, region=self.speech_region
            )
            self.synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config, audio_config=None
            )
        except Exception as e:
            pass

    def on_play_clicked(self):
        self.text = self.playwidget.textEdit_text.toPlainText()
        self.ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.language_type}">'
            f'<voice name="{self.language_type}-{self.voice}">'
            f'<prosody rate="{self.voice_speed}">'
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
