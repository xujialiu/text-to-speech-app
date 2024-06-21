import sys
import keyboard
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Press F3 to see a message", self)
        self.setCentralWidget(self.label)
        self.setWindowTitle("Global Hotkey Example")
        self.resize(300, 200)

        # Set up the global hotkey
        keyboard.add_hotkey('F3', self.on_f3_pressed)

    def on_f3_pressed(self):
        self.label.setText("F3 key pressed!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
