import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCT_SERVICE_URL = "http://localhost:5001" 

orders = {}

TIMEOUT_SECONDS = 5


@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data.get('product_id')

    try:
        response = requests.post(f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            product_data = response.json()
            order_id = len(orders) + 1 
            order = {
                "id": order_id,
                "product_id": product_id,
                "product_name": product_data['name'],
                "product_price": product_data['price'],
            }
            orders[order_id] = order
            return jsonify({"message": "Order created", "order": order}), 201
        else:
            return jsonify({"error": "Product not found"}), 404
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Product Service timed out"}), 500


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{order_id}", timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Order not found"}), 404
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Product Service timed out"}), 500


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    try:
        response = requests.put(f"{PRODUCT_SERVICE_URL}/products/{order_id}", json=data, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to update the order"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Product Service timed out"}), 500


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    try:
        response = requests.delete(f"{PRODUCT_SERVICE_URL}/products/{order_id}", timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to cancel the order"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to Product Service timed out"}), 500



#http POST http://localhost:5002/orders product_id:=2
#http GET http://localhost:5002/orders/1
#http PUT http://localhost:5002/orders/1 product_id:=3
#http DELETE http://localhost:5002/orders/1

