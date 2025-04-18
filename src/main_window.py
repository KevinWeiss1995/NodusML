from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton)
from PyQt6.QtCore import Qt
from components.node_table import NodeTableWidget
from components.metrics_plot import MetricsPlotWidget
from components.control_panel import ControlPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Distributed ML Monitor")
        self.resize(1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left panel for node table and controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.node_table = NodeTableWidget()
        self.control_panel = ControlPanel()
        
        left_layout.addWidget(self.node_table)
        left_layout.addWidget(self.control_panel)
        
        # Right panel for metrics visualization
        self.metrics_plot = MetricsPlotWidget()
        
        # Add panels to main layout
        layout.addWidget(left_panel, stretch=40)
        layout.addWidget(self.metrics_plot, stretch=60) 