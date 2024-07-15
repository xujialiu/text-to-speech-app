import multiprocessing
import sys
from PySide6.QtWidgets import QApplication
from MainWindowImpl import MainWindowImpl



multiprocessing.freeze_support()  # This is necessary for Windows
app = QApplication(sys.argv)
window = MainWindowImpl()
window.show()
sys.exit(app.exec())