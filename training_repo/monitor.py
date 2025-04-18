import requests
import psutil
import GPUtil
import time
import socket
from threading import Thread
from urllib3.util import connection
import urllib3

# Force IPv6
def allowed_gai_family():
    return socket.AF_INET6

connection.allowed_gai_family = allowed_gai_family

class TrainingMonitor:
    def __init__(self, node_id=None, server_url="http://localhost:5000", 
                 username='admin', password='your_secure_password', retry_interval=5):
        self.node_id = node_id or socket.gethostname()
        self.server_url = server_url
        self.auth = (username, password)
        self.running = True
        self.mode = "local" if "localhost" in server_url else "distributed"
        self.retry_interval = retry_interval
        self.session = requests.Session()
        
    def send_metrics(self, metrics):
        """Send training metrics (loss, accuracy etc)"""
        data = {
            "node_id": self.node_id,
            "timestamp": time.time(),
            "mode": self.mode,
            **metrics,
            "status": "training",
            "cpu_usage": psutil.cpu_percent(),
            "gpu_usage": GPUtil.getGPUs()[0].load * 100 if GPUtil.getGPUs() else 0
        }
        while self.running:
            try:
                response = self.session.post(
                    f"{self.server_url}/metrics", 
                    json=data, 
                    auth=self.auth,
                    timeout=5
                )
                if response.status_code == 200:
                    break
                print(f"Failed to send metrics: {response.status_code}")
            except Exception as e:
                print(f"Connection error to {self.server_url}: {e}")
            time.sleep(self.retry_interval)


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