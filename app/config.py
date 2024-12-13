import json
from flask import Flask, request, jsonify
import requests
from uuid import uuid4

app = Flask(__name__)

# Примерные URL для различных микросервисов
RPC_SERVICES = {
    "calc.summ": "http://localhost:5003/summ",
    "calc.sub": "http://localhost:5003/sub",
    "calc.mult": "http://localhost:5003/mult",
    "calc.div": "http://localhost:5003/div"
}

@app.route('/rpc', methods=['POST'])
def handle_rpc():
    try:
        # Получаем JSON объект из тела запроса
        data = request.json

        # Проверяем, что в запросе присутствует метод и данные
        if "method" not in data or "data" not in data or "requestId" not in data:
            return jsonify({"error": "Missing required fields"}), 400

        method = data["method"]
        request_id = data["requestId"]
        method_url = RPC_SERVICES.get(method)

        # Проверяем, что такой метод существует
        if not method_url:
            return jsonify({"error": f"Method {method} not supported"}), 404

        # Прокси запрос в соответствующий микросервис
        response = requests.post(method_url, json=data["data"])

        # Проверяем статус ответа микросервиса
        if response.status_code != 200:
            return jsonify({"error": f"Error in calling service: {response.text}"}), response.status_code

        # Возвращаем ответ от микросервиса
        return jsonify({
            "requestId": request_id,
            "result": response.json()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Запуск RPC Gateway на порту 5001
