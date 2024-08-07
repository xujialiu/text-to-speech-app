# -*- coding: utf-8 -*-
# TODO:


import json
import multiprocessing
from pathlib import Path
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
)
from PySide6.QtCore import QSettings

import MainWindow
import PlayWidget
import SetWidget
import DebugWidget
from pynput import keyboard
import pyautogui
from TTSPlayer import MyAudioPlayer, MySpeechSynthesizer, Speech2MP3
import VERSION


class MainWindowImpl(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        self.convert = 0
        self.play_pause = 0
        self.global_hotkeys_listener = None
        self.dict_fn_hotkey = {
            self.on_start_conv_hotkey_triggered: None,
            self.on_pause_resume_hotkey_triggered: None,
            self.on_stop_hotkey_triggered: None,
        }
        self.dict_hotkey_fn = dict()

        self.init_ui()
        self.read_settings()
        self.init_tts()
        

    def init_ui(self):
        self._init_app()
        self._init_mainwindow()
        self._init_playwidget()
        self._init_setwidget()
        
        if self.debug:
            self._init_debugwidget()
        else:
            idx = self.mainwindow.tabWidget.indexOf(self.mainwindow.tab_debug)
            self.mainwindow.tabWidget.setTabVisible(idx, False)

        self._init_tray_menu()
        self._init_tray_icon()

        self._init_stop_conv_button()
        self._init_start_conv_button()
        self._init_pause_resume_button()

        self._init_keysequenceedit()

        self._init_speech_region()
        self._init_speech_key()
        self._init_language_type()
        self._init_voice_type()
        self._init_voice_speech()
        self._init_clipboard()

        self._init_save_button()
        self._init_select_folder_button()

    def init_tts(self):
        self.speech_synthesizer = None
        self.audio_process = None
        self.is_converting = multiprocessing.Value("b", False)
        self.is_paused = multiprocessing.Value("b", False)
        self.process_synthesizer = None
        self.process_player = None

    # working
    def _init_save_button(self):
        self.playwidget.pushButton_save.clicked.connect(self.on_save_clicked)

    def on_save_clicked(self):
        """点击save, 启动一个进程, 保存为mp3"""
        self.get_file_path()
        text = self.playwidget.textEdit_text.toPlainText()
        self.generate_ssml(text)
        print(self.file_path.__str__())
        # 添加转换完成的提示框, 需要用到qthread
        result = Speech2MP3(self.speech_key, self.speech_region, self.ssml, str(self.file_path))

    def get_file_path(self):
        self.folder = Path(self.folder_text)
        idx = 1
        while True:
            self.file_path = self.folder / f"text-to-speech_{idx}.mp3"
            if not self.file_path.exists():
                break
            idx += 1
        print(self.file_path)

    def _init_select_folder_button(self):
        self.playwidget.pushButton_select_folder.clicked.connect(
            self.on_select_folder_clicked
        )

    def on_select_folder_clicked(self):
        self.folder_text = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if self.folder_text:
            self.playwidget.lineEdit_folder.setText(self.folder_text)

    def _init_stop_conv_button(self):
        self.playwidget.pushButton_stop_conv.clicked.connect(self.on_stop_conv_clicked)

    def _init_start_conv_button(self):
        self.playwidget.pushButton_start_conv.clicked.connect(
            self.on_start_conv_clicked
        )

    def _init_pause_resume_button(self):
        self.playwidget.pushButton_pause_resume.clicked.connect(
            self.on_pause_resume_clicked
        )

    def _init_speech_key(self):
        self.setwidget.lineEdit_speech_key.textChanged.connect(
            self.on_speech_key_changed
        )

    def on_speech_key_changed(self, text):
        self.speech_key = text

    def _init_speech_region(self):
        self.setwidget.lineEdit_speech_region.textChanged.connect(
            self.on_speech_region_changed
        )

    def on_speech_region_changed(self, text):
        self.speech_region = text

    def _init_clipboard(self):
        self.clipboard = QApplication.clipboard()

    def _init_keysequenceedit(self):
        self.setwidget.keySequenceEdit_start_conv.keySequenceChanged.connect(
            self.set_convert_hotkey
        )
        self.setwidget.keySequenceEdit_stop_conv.keySequenceChanged.connect(
            self.set_stop_hotkey
        )
        self.setwidget.keySequenceEdit_pause_resume.keySequenceChanged.connect(
            self.set_pasue_resume_hotkey
        )

    # 关于快捷键的逻辑------
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

    @staticmethod
    def convert_keysequence_to_string(keysequenceedit):
        return keysequenceedit.keySequence().toString(QKeySequence.NativeText)

    def set_convert_hotkey(self):
        str_keysequence_convert = self.convert_keysequence_to_string(
            self.setwidget.keySequenceEdit_start_conv
        )
        self.set_hotkey(str_keysequence_convert, self.on_start_conv_hotkey_triggered)

    def set_stop_hotkey(self):
        str_keysequence_stop = self.convert_keysequence_to_string(
            self.setwidget.keySequenceEdit_stop_conv
        )
        self.set_hotkey(str_keysequence_stop, self.on_stop_hotkey_triggered)

    def set_pasue_resume_hotkey(self):
        str_keysequence_pause_resume = self.convert_keysequence_to_string(
            self.setwidget.keySequenceEdit_pause_resume
        )
        self.set_hotkey(
            str_keysequence_pause_resume, self.on_pause_resume_hotkey_triggered
        )

    def on_pause_resume_hotkey_triggered(self):
        self.on_pause_resume_clicked()

    def on_stop_hotkey_triggered(self):
        """按下stop converting and pause, 停止转换文本"""
        self.stop_conv()
        self.stop_play()

    def on_start_conv_hotkey_triggered(self):
        """按下start converting, 从剪切板获取文本并转换成语音"""
        text = self.clipboard.text()
        self.start_conv_and_play(text)

    # 关于快捷键的逻辑------

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
        print("debug")

    def _init_tray_menu(self):
        self.tray_menu = QMenu()
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.on_close_clicked)
        self.tray_menu.addAction(close_action)

    def _init_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)  # 设置系统托盘图标
        self.tray_icon.setToolTip("Azure-Text-To-Speech")

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show()

    def on_close_clicked(self):
        """真正的关闭事件"""
        self.on_stop_conv_clicked()
        # 清理资源
        if self.process_synthesizer:
            self.process_synthesizer.terminate()
            self.process_synthesizer.close()
        if self.process_player:
            self.process_player.terminate()
            self.process_player.close()

        self.tray_icon.hide()
        # save settings before closed
        self.write_settings()
        self.global_hotkeys_listener.stop()
        QApplication.quit()

    def _load_meta_json(self):
        """加载语音信息"""
        file_path = ".meta/meta.json"
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
        self.voice_speed = self.setwidget.doubleSpinBox_voice_speed.text()
        self.setwidget.doubleSpinBox_voice_speed.valueChanged.connect(
            self.on_voice_speed_changed
        )

    def on_voice_speed_changed(self, value):
        self.voice_speed = value

    def _init_mainwindow(self):
        self.mainwindow = MainWindow.Ui_MainWindow()
        self.mainwindow.setupUi(self)
        self.icon = QIcon(".meta/icon.ico")
        self.setWindowIcon(self.icon)

    def _init_playwidget(self):
        self.playwidget = PlayWidget.Ui_Form()
        self.playwidget.setupUi(self.mainwindow.tab_play)

        self._init_start_conv_button()

    def _init_setwidget(self):
        self.setwidget = SetWidget.Ui_Form()
        self.setwidget.setupUi(self.mainwindow.tab_setting)

    def closeEvent(self, event):
        """点击主窗口右上角的x的事件, 并非真正的关闭事件"""
        """暂时不实现上面的逻辑, 按照正常标准退出"""
        # event.ignore()
        # self.hide()
        # self.tray_icon.showMessage(
        #     "Azure-Text-To-Speech",
        #     "The program has been minimized to the system tray.",
        #     QSystemTrayIcon.Information,
        #     2000,
        # )
        self.write_settings()

        self.on_stop_conv_clicked()
        # 清理资源
        if self.process_synthesizer:
            self.process_synthesizer.terminate()
            self.process_synthesizer.close()
        if self.process_player:
            self.process_player.terminate()
            self.process_player.close()

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

        convert_key_sequence = settings.value("start_converting", "")
        if convert_key_sequence:
            self.setwidget.keySequenceEdit_start_conv.setKeySequence(
                QKeySequence(convert_key_sequence)
            )

        stop_key_sequence = settings.value("stop_converting", "")
        if stop_key_sequence:
            self.setwidget.keySequenceEdit_stop_conv.setKeySequence(
                QKeySequence(stop_key_sequence)
            )

        stop_key_sequence = settings.value("pause / resume", "")
        if stop_key_sequence:
            self.setwidget.keySequenceEdit_pause_resume.setKeySequence(
                QKeySequence(stop_key_sequence)
            )
            
        # read select folder setting
        self.folder_text = settings.value("select folder", "")
        self.playwidget.lineEdit_folder.setText(self.folder_text)

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
            "start_converting",
            self.setwidget.keySequenceEdit_start_conv.keySequence(),
        )

        settings.setValue(
            "stop_converting", self.setwidget.keySequenceEdit_stop_conv.keySequence()
        )

        settings.setValue(
            "pause / resume", self.setwidget.keySequenceEdit_pause_resume.keySequence()
        )
        
        settings.setValue(
            "select folder", self.folder_text
        )

    # working!!!
    def on_start_conv_clicked(self):
        text = self.playwidget.textEdit_text.toPlainText()
        self.start_conv_and_play(text)

    def on_start_conv_hotkey_clicked(self):
        text = self.clipboard.text()
        self.start_conv_and_play(text)

    def start_conv_and_play(self, text):
        self.on_stop_conv_clicked()
        self.audio_queue = (
            multiprocessing.Queue()
        )  # 尝试使用multiprocessing.Manager代替它

        # self.audio_queue = multiprocessing.Manager().Queue()
        self.is_converting.value = True
        self.is_paused.value = False
        speech_key = self.setwidget.lineEdit_speech_key.text()
        service_region = self.setwidget.lineEdit_speech_region.text()

        self.generate_ssml(text)

        # 创建synthesizer进程
        self.process_synthesizer = MySpeechSynthesizer(
            speech_key, service_region, self.audio_queue, self.ssml
        )
        self.process_synthesizer.start()

        # 创建player进程
        self.process_player = MyAudioPlayer(
            self.audio_queue, self.is_converting, self.is_paused
        )
        self.process_player.start()

    def generate_ssml(self, text):
        self.ssml = (
            f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{self.language_type}">'
            f'<voice name="{self.language_type}-{self.voice}">'
            f'<prosody rate="{self.voice_speed}">'
            f"{text}"
            "</prosody>"
            "</voice>"
            "</speak>"
        )

    def stop_conv(self):
        if self.process_synthesizer:
            try:
                self.process_synthesizer.terminate()
            except AttributeError:
                pass

        self.is_converting.value = False

    def stop_play(self):
        if self.process_player:
            try:
                self.process_player.terminate()
            except AttributeError:
                pass

        self.is_paused.value = False

    def on_stop_conv_clicked(self):
        self.stop_conv()
        self.stop_play()

    def on_pause_resume_clicked(self):
        if self.is_paused.value:
            self.is_paused.value = False
        else:
            self.is_paused.value = True

    def _init_app(self):
        app = QApplication.instance()
        app.setStyle("fusion")


# 仅用于测试
if __name__ == "__main__":
    import sys

    multiprocessing.freeze_support()  # This is necessary for Windows
    app = QApplication(sys.argv)
    window = MainWindowImpl(debug=True)
    window.show()
    sys.exit(app.exec())
