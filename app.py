from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'locations.json')

def load_locations():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print("❌ 讀取 JSON 失敗:", e)
        return []

def save_locations(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

locations = load_locations()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    # 送 locations 給地圖顯示
    return render_template('logs.html', locations=locations)

@app.route('/save-location', methods=['POST'])
def save_location():
    try:
        data = request.json
        user_id = data.get('user_id', 'unknown')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({'status': 'error', 'msg': '資料錯誤'})

        timestamp = datetime.now().isoformat()
        locations.append({
            'user_id': user_id,
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': timestamp
        })
        save_locations(locations)

        print("🔥 收到資料：", {'user_id': user_id, 'latitude': latitude, 'longitude': longitude, 'timestamp': timestamp})
        return jsonify({'status': 'success'})

    except Exception as e:
        print("❌ 錯誤：", e)
        return jsonify({'status': 'error', 'msg': str(e)})

# ✅ 提供即時 JSON API
@app.route('/logs-data')
def logs_data():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
