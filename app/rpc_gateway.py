from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Логирование
logger = logging.getLogger("RPC Gateway")

# Конфигурация микросервисов
MICROSERVICES = {
    "calc.summ": "http://localhost:5002/calc",
    "calc.sub": "http://localhost:5002/calc",
    "calc.mult": "http://localhost:5002/calc",
    "calc.div": "http://localhost:5002/calc",
}

@app.route('/rpc', methods=['POST'])
def rpc_handler():
    try:
        data = request.get_json()
        logger.info(f"Получен запрос: {data}")

        # Проверка данных
        method = data.get("method")
        request_id = data.get("requestId")
        if not method or not request_id:
            logger.error("Неверный запрос: отсутствует метод или requestId")
            return jsonify({"error": "Invalid request"}), 400

        # Получение URL микросервиса
        service_url = MICROSERVICES.get(method)
        if not service_url:
            logger.error(f"Сервис не найден для метода {method}")
            return jsonify({"error": f"No service found for method {method}"}), 404

        # Прокси