from flask import Flask, request, jsonify
from prometheus_client import Counter, Summary, start_http_server
import time

app = Flask(__name__)

# Метрики для Prometheus
REQUEST_COUNT = Counter('calc_service_requests_total', 'Общее количество запросов в calc_service', ['method'])
REQUEST_LATENCY = Summary('calc_service_request_latency_seconds', 'Время обработки запроса в секундах')
ERROR_COUNT = Counter('calc_service_errors_total', 'Количество ошибок в calc_service', ['method'])


# Эндпоинт для Prometheus
@app.route('/metrics', methods=['GET'])
def metrics():
    from prometheus_client import generate_latest
    return generate_latest()


@app.route('/calc', methods=['POST'])
@REQUEST_LATENCY.time()  # Замер времени выполнения
def calc_service():
    try:
        data = request.get_json()
        method = data.get("method")
        args = data.get("data", {}).get("args", [])

        REQUEST_COUNT.labels(method=method).inc()  # Увеличиваем счетчик запросов

        if method == "calc.summ":
            result = sum(args)
        elif method == "calc.sub":
            result = args[0] - sum(args[1:])
        elif method == "calc.mult":
            result = 1
            for num in args:
                result *= num
        elif method == "calc.div":
            result = args[0]
            for num in args[1:]:
                if num == 0:
                    ERROR_COUNT.labels(method=method).inc()  # Увеличиваем счетчик ошибок
                    return jsonify({"error": "Division by zero"}), 400
                result /= num
        else:
            ERROR_COUNT.labels(method=method).inc()  # Увеличиваем счетчик ошибок
            return jsonify({"error": "Unknown method"}), 404

        return jsonify({"requestId": data.get("requestId"), "result": result})
    except Exception as e:
        ERROR_COUNT.labels(method="unknown").inc()  # Увеличиваем счетчик ошибок
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    start_http_server(9102)  # Prometheus сервер будет слушать на порту 9102
    app.run(port=5002)
