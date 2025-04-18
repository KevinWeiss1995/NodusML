from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal

class ControlPanel(QWidget):
    start_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        
        self.start_btn = QPushButton("Start Training")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        
        layout.addWidget(self.start_btn)
        layout.addWidget(self.pause_btn)
        layout.addWidget(self.stop_btn)
        
        self.setup_connections()
    
    def setup_connections(self):
        self.start_btn.clicked.connect(self.start_signal.emit)
        self.pause_btn.clicked.connect(self.pause_signal.emit)
        self.stop_btn.clicked.connect(self.stop_signal.emit) 