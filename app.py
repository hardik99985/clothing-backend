from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import datetime

app = Flask(__name__)
CORS(app)

# Hardcoded login credentials
USERNAME = "hardik"
PASSWORD = "hardik123"

# Orders file
ORDERS_FILE = "orders.json"

# Load orders from file
def load_orders():
    try:
        with open(ORDERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

# Save orders to file
def save_orders(orders):
    with open(ORDERS_FILE, 'w') as f:
        json.dump(orders, f, indent=2)

# 📌 1. POST /order – Save order from frontend
@app.route("/order", methods=["POST"])
def receive_order():
    data = request.json
    data["id"] = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    orders = load_orders()
    orders.append(data)
    save_orders(orders)
    return jsonify({"success": True, "order_id": data["id"]})

# 📌 2. POST /login – Dashboard login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data.get("username") == USERNAME and data.get("password") == PASSWORD:
        return jsonify({"success": True})
    return jsonify({"success": False})

# 📌 3. GET /orders – Get all orders (no session, open access)
@app.route("/orders")
def orders():
    return jsonify(load_orders())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
