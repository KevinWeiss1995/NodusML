from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtCore import QTimer
import requests

class NodeTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setup_table()
        self.setup_update_timer()
    
    def setup_table(self):
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels([
            "Node ID", "Status", "CPU Usage", "GPU Usage"
        ])
        self.horizontalHeader().setStretchLastSection(True)
    
    def setup_update_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_node_status)
        self.timer.start(1000)  # Update every second
    
    def update_node_status(self):
        try:
            response = requests.get("http://localhost:5000/status")
            nodes = response.json()
            
            self.setRowCount(len(nodes))
            for i, (node_id, status) in enumerate(nodes.items()):
                self.setItem(i, 0, QTableWidgetItem(node_id))
                self.setItem(i, 1, QTableWidgetItem(status['status']))
                self.setItem(i, 2, QTableWidgetItem(f"{status['cpu_usage']:.1f}%"))
                self.setItem(i, 3, QTableWidgetItem(f"{status['gpu_usage']:.1f}%"))
        except Exception as e:
            print(f"Error updating node status: {e}") 