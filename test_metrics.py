from training_repo.monitor import TrainingMonitor
import time
import math

monitor = TrainingMonitor("test_node")

for i in range(100):
    metrics = {
        "loss": math.exp(-i/20) + 0.1,
        "accuracy": 1 - math.exp(-i/20),
    }
    monitor.send_metrics(metrics)
    time.sleep(0.5) 