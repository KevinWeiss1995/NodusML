from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
from PyQt6.QtCore import QTimer
import requests
import numpy as np

class MetricsPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setTitle("Training Metrics")
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'Time')
        
        layout.addWidget(self.plot_widget)
        
        self.curves = {}
        self.data = {'loss': [], 'accuracy': []}

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_metrics)
        self.timer.start(1000) 
     
        self.max_points = 100
        self.timestamps = []
    
    def update_metrics(self):
        try:
            response = requests.get("http://localhost:5000/metrics")
            data = response.json()
            
            if data and 'timestamp' in data:
                self.timestamps.append(data['timestamp'])
                self.data['loss'].append(data['loss'])
                self.data['accuracy'].append(data['accuracy'])
            
                if len(self.timestamps) > self.max_points:
                    self.timestamps = self.timestamps[-self.max_points:]
                    self.data['loss'] = self.data['loss'][-self.max_points:]
                    self.data['accuracy'] = self.data['accuracy'][-self.max_points:]
            
                if 'loss' not in self.curves:
                    self.curves['loss'] = self.plot_widget.plot(pen='r', name='Loss')
                    self.curves['accuracy'] = self.plot_widget.plot(pen='b', name='Accuracy')
                
                self.curves['loss'].setData(self.timestamps, self.data['loss'])
                self.curves['accuracy'].setData(self.timestamps, self.data['accuracy'])
            
        except Exception as e:
            print(f"Error updating metrics: {e}") 