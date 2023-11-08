from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

products = {
    1: {"id": 1, "name": "Product A", "price": 10.0, "stock": 100},
    2: {"id": 2, "name": "Product B", "price": 15.0, "stock": 50},
    3: {"id": 3, "name": "Product C", "price": 20.0, "stock": 75},
}

REQUEST_TIMEOUT = 5

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product_id = len(products) + 1
    product = {"id": product_id, "name": data['name'], "price": data['price'], "stock": data['stock']}
    
    try:
        response = requests.post('http://localhost:5001/products', json=product, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 201:
            products[product_id] = product
            return jsonify({"message": "Product created", "product": product}), 201
        else:
            return jsonify({"error": "External service error"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "External service request timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"External service request failed: {e}"}), 500


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        response = requests.get(f'http://localhost:5001/products/{product_id}', timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({"error": "Product not found"}), 404
        else:
            return jsonify({"error": "External service error"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "External service request timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"External service request failed: {e}"}), 500

    
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    
    try:
        response = requests.put(f'http://localhost:5001/products/{product_id}', json=data, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({"error": "Product not found"}), 404
        else:
            return jsonify({"error": "External service error"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "External service request timed out"}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"External service request failed: {e}"}), 500


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products.pop(product_id, None)
    if product:
        return jsonify({"message": "Product deleted", "product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(port=5001)



#http POST http://localhost:5001/products name="New Product" price:=25.0   
#http GET http://localhost:5001/products/1
#http DELETE http://localhost:5001/products/1
#http PUT http://localhost:5001/products/2 name="Updated Product A" price:=12.0


