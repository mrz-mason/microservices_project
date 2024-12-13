from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Логирование
logger = logging.getLogger("Load Balancer")

# Конфигурация маршрутов
ROUTES = {
    "/rpc": "http://localhost:5001/rpc",
    "/static": "http://localhost:5003/static",
}

@app.route('/<path:path>', methods=['GET', 'POST'])
def route_handler(path):
    try:
        target_url = ROUTES.get(f"/{path}")
        if not target_url:
            logger.error(f"Путь {path} не найден")
            return jsonify({"error": "Path not found"}), 404

        # Проксирование запроса
        if request.method == 'POST':
            response = requests.post(target_url, json=request.get_json())
        else:
            response = requests.get(target_url)

        logger.info(f"Запрос к {target_url}: {response.status_code}")
        return response.content, response.status_code, response.headers.items()

    except Exception as e:
        logger.error(f"Ошибка в Load Balancer: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
