from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import queue

app = Flask(__name__)
CORS(app)

# Global queue to store latest metrics
metrics_queue = queue.Queue()
node_statuses = {}
latest_metrics = {}

@app.route('/metrics', methods=['GET', 'POST'])
def metrics():
    if request.method == 'POST':
        data = request.json
        metrics_queue.put(data)
        node_statuses[data['node_id']] = {
            'status': data['status'],
            'cpu_usage': data['cpu_usage'],
            'gpu_usage': data['gpu_usage']
        }
        latest_metrics.update(data)
        return jsonify({'status': 'ok'})
    else:
        return jsonify(latest_metrics)

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(node_statuses)

def run_server():
    app.run(host='0.0.0.0', port=5000)

def start_server():
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    return metrics_queue 