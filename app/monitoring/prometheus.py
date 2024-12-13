from prometheus_client import start_http_server, Summary
import time

# Метрика для отслеживания времени обработки запросов
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


@app.route('/rpc', methods=['POST'])

@REQUEST_TIME.time()  # Добавляем метрику
def handle_rpc(request):
    data = request.json
    # Время выполнения запроса будет автоматически засчитано в метрику
    return jsonify({"message": "Request processed"})
