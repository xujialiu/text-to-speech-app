# main.py
import sys
from PySide6.QtWidgets import QApplication
from MainWindowImpl import MainWindowImpl


# TEST_MODE = True

app = QApplication(sys.argv)
mwImpl = MainWindowImpl()
mwImpl.show()
sys.exit(app.exec())