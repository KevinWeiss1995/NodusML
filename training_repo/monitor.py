import requests
import psutil
import GPUtil
import time
from threading import Thread

class TrainingMonitor:
    def __init__(self, node_id, server_url="http://localhost:5000"):
        self.node_id = node_id
        self.server_url = server_url
        self.running = True
        
    def send_metrics(self, metrics):
        """Send training metrics (loss, accuracy etc)"""
        data = {
            "node_id": self.node_id,
            "timestamp": time.time(),
            **metrics,
            "status": "training",
            "cpu_usage": psutil.cpu_percent(),
            "gpu_usage": GPUtil.getGPUs()[0].load * 100 if GPUtil.getGPUs() else 0
        }
        try:
            requests.post(f"{self.server_url}/metrics", json=data)
        except:
            print("Failed to send metrics")

# Usage in your training loop:
"""
monitor = TrainingMonitor("node1")

for epoch in epochs:
    for batch in data:
        # Your training code...
        metrics = {
            "loss": current_loss,
            "accuracy": current_accuracy,
        }
        monitor.send_metrics(metrics)
""" 