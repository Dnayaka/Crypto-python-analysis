import requests
import time
import csv
import os
import threading
import glob
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

# ====== KONFIGURASI ======
app = Flask(__name__)
CORS(app)

COINS = [
    "bitcoin", "ethereum", "binancecoin", "ripple", "cardano", "solana",
    "dogecoin", "polkadot", "shiba-inu", "matic-network",
    "tron", "avalanche-2", "near", "aptos", "hedera-hashgraph",
    "algorand", "cosmos", "vechain", "tezos", "kaspa",
    "chainlink", "uniswap", "aave", "curve-dao-token", "rocket-pool",
    "the-graph", "injective-protocol", "pancakeswap-token", "synthetix-network-token",
    "tether", "usd-coin", "dai", "true-usd",
    "litecoin", "stellar", "bitcoin-cash", "monero", "dash", "zcash",
    "floki", "pepe", "dogelon-mars", "bonk", "fartcoin"
]
CURRENCY = "idr"
API_URL = "https://api.coingecko.com/api/v3/simple/price"
CSV_FOLDER = "scan_history"
FETCH_INTERVAL = 14400  # 4 jam dalam detik (bukan 5 menit)
KEEP_LATEST_ONLY = True  # Hanya simpan file terbaru

# Buat folder jika belum ada
os.makedirs(CSV_FOLDER, exist_ok=True)

# ====== FUNGSI UTAMA ======
def fetch_crypto_data():
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": CURRENCY,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true"
    }
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def calculate_signal(momentum):
    if momentum > 2:
        return "HIGH BUY"
    elif momentum < -2:
        return "LOW SELL"
    else:
        return "MEDIUM HOLD"

def predict_next_price(current_price, momentum):
    change_factor = 1 + (min(max(momentum, -10), 10) / 100)
    return current_price * change_factor

def cleanup_old_files():
    # Hapus semua file lama jika hanya ingin menyimpan yang terbaru
    if KEEP_LATEST_ONLY:
        csv_files = glob.glob(os.path.join(CSV_FOLDER, "crypto_data_*.csv"))
        for file in csv_files:
            os.remove(file)
            print(f"Deleted old file: {file}")

def save_crypto_data():
    data = fetch_crypto_data()
    if data:
        # Hapus file lama sebelum menyimpan yang baru
        cleanup_old_files()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(CSV_FOLDER, f"crypto_data_{timestamp}.csv")
        
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["coin", "signal", "price", "volume", "momentum", "next_price", "score", "timestamp"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for coin_id, info in data.items():
                price = info.get(f"{CURRENCY}", 0)
                volume = info.get(f"{CURRENCY}_24h_vol", 0)
                momentum = info.get(f"{CURRENCY}_24h_change", 0)
                
                signal = calculate_signal(momentum)
                next_price = predict_next_price(price, momentum)
                score = volume * abs(momentum)
                
                writer.writerow({
                    "coin": coin_id.capitalize(),
                    "signal": signal,
                    "price": price,
                    "volume": volume,
                    "momentum": momentum,
                    "next_price": next_price,
                    "score": score,
                    "timestamp": timestamp
                })
        
        print(f"Data saved: {filename}")
        return True
    return False

def auto_fetch_data():
    while True:
        save_crypto_data()
        time.sleep(FETCH_INTERVAL)

def load_latest_csv_data():
    # Hanya muat file terbaru
    csv_files = glob.glob(os.path.join(CSV_FOLDER, "crypto_data_*.csv"))
    if not csv_files:
        return []
    
    # Dapatkan file terbaru
    latest_file = max(csv_files, key=os.path.getctime)
    
    all_data = []
    with open(latest_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_data.append(row)
    
    return all_data

# ====== ROUTES FLASK ======
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = load_latest_csv_data()
    return jsonify(data)

@app.route('/api/fetch')
def manual_fetch():
    if save_crypto_data():
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/api/export')
def export_data():
    data = load_latest_csv_data()
    export_filename = os.path.join(CSV_FOLDER, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    with open(export_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["coin", "signal", "price", "volume", "momentum", "next_price", "score", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    return send_file(export_filename, as_attachment=True)

# ====== EKSEKUSI PROGRAM ======
if __name__ == "__main__":
    # Cek jika sedang dalam mode debug/reload
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
        # Jalankan thread untuk auto-fetch hanya sekali
        fetch_thread = threading.Thread(target=auto_fetch_data, daemon=True)
        fetch_thread.start()
    
    # Jalankan Flask app
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)