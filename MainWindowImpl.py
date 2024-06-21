from PySide6.QtWidgets import QWidget
import MainWindow

class MainWindowImpl(QWidget):
    def __init__(self, parent=None):
        super(MainWindowImpl, self).__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self._init_mainwindow()
        self._init_debug_tab()
    
    
    def _init_mainwindow(self):
        self.mainwindow = MainWindow.Ui_Form()
        self.mainwindow.setupUi(self)
    
    def _init_debug_tab(self):
        self.mainwindow.pushButton_debug.clicked.connect(self.on_debug_clicked)
        
    def on_debug_clicked(self):
        try:
            exec(f"print({self.mainwindow.lineEdit_debug.text()})")
        except Exception as e:
            print(e)
    
    
    
    
    
        