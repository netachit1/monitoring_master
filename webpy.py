from flask import Flask, render_template, jsonify
import json
from datetime import datetime
import os

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('index.html')


@app.route('/api/monitoring')
def get_monitoring_data():
    try:
        with open('monitoring_data.json', 'r') as f:
            data = json.load(f)

            if not isinstance(data, list):
                data = [data]

            # فقط آخرین ۳۰ رکورد برای نمودار
            if len(data) > 30:
                data = data[-30:]

            formatted_data = []
            for item in data:
                connections = 0
                if 'net' in item and isinstance(item['net'], list) and len(item['net']) > 7:
                    connections = item['net'][7]

                timestamp = item.get('timestamp')
                if not timestamp and 'boot_seconds' in item:
                    timestamp = datetime.fromtimestamp(item['boot_seconds']).strftime("%Y-%m-%d %H:%M:%S")

                record = {
                    "timestamp": timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "cpu": round(item.get('cpu', 0), 1),
                    "mem": round(item.get('mem', 0), 1),
                    "disk": round(item.get('disk', 0), 1),
                    "connections": connections
                }
                formatted_data.append(record)

            return jsonify(formatted_data)

    except Exception as e:
        print(f"خطا: {e}")
        return jsonify([])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)