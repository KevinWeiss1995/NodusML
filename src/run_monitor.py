from backend.metrics_server import start_server
from main import main
import time

if __name__ == "__main__":
    # Start the metrics server first
    metrics_queue = start_server()
    
    # Give the server a moment to start
    time.sleep(1)
    
    # Launch the GUI
    main() 