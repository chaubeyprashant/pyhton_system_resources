from flask import Flask, jsonify
import psutil
import GPUtil
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_cpu_usage():
    logging.debug("Fetching CPU usage")
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.debug("CPU usage: %s%%" % cpu_usage)  # Updated to use `%` formatting
    return cpu_usage

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
        logging.debug("GPU data: %s" % gpu_data)  # Updated to use `%` formatting
        return gpu_data
    except Exception as e:
        logging.error("Error fetching GPU usage: %s" % e)  # Updated to use `%` formatting
        return [{"error": str(e)}]

@app.route('/system_resources')
def system_resources():
    try:
        cpu_usage = get_cpu_usage()
        gpu_usage = get_gpu_usage()
        
        system_resources_data = {
            "cpu_usage": cpu_usage,
            "gpu_usage": gpu_usage
        }
        
        return jsonify(system_resources_data)
    
    except Exception as e:
        logging.error("Error in /system_resources endpoint: %s" % e)  # Updated to use `%` formatting
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    logging.info("Starting Flask server")
    app.run(host='localhost', port=5001, threaded=True)
