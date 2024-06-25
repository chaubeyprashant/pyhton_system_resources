from flask import Flask, jsonify
import psutil
import GPUtil
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import errno

# Initialize Flask app
app = Flask(__name__)

# Ensure logs directory exists
logs_dir = 'logs'

try:
    os.makedirs(logs_dir)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# Configure logging
log_file = os.path.join(logs_dir, 'resource_usage.log')

handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
handler.setLevel(logging.DEBUG)

logging.getLogger().addHandler(handler)
logging.basicConfig(level=logging.DEBUG)

def get_cpu_usage():
    logging.debug("Fetching CPU usage")
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        logging.debug("CPU usage: %s%%" % cpu_usage)
        return cpu_usage
    except Exception as e:
        logging.error("Error fetching CPU usage: %s" % e)
        raise

def get_gpu_usage():
    logging.debug("Fetching GPU usage")
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            logging.warning("No GPUs found")
            return []
        gpu_data = []
        for gpu in gpus:
            gpu_data.append({
                "id": gpu.id,
                "name": gpu.name,
                "load": gpu.load * 100,
                "memoryUtil": gpu.memoryUtil * 100
            })
        logging.debug("GPU data: %s" % gpu_data)
        return gpu_data
    except Exception as e:
        logging.error("Error fetching GPU usage: %s" % e)
        raise

@app.route('/system_resources')
def system_resources():
    try:
        cpu_usage = get_cpu_usage()
        gpu_usage = get_gpu_usage()
        
        system_resources_data = {
            "cpu_usage": cpu_usage,
            "gpu_usage": gpu_usage
        }
        
        logging.info("Resource usage data: CPU %s%%, GPUs %s" % (cpu_usage, gpu_usage))
        
        return jsonify(system_resources_data)
    
    except Exception as e:
        logging.error("Error in /system_resources endpoint: %s" % e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logging.info("Starting Flask server")
    app.run(host='localhost', port=5001, threaded=True)
