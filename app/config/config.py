# Конфигурация приложения
import os

RPC_GATEWAY_PORT = os.getenv("RPC_GATEWAY_PORT", 5001)
LOAD_BALANCER_PORT = os.getenv("LOAD_BALANCER_PORT", 5000)
CALC_SERVICE_PORT = os.getenv("CALC_SERVICE_PORT", 5002)
STATIC_SERVICE_PORT = os.getenv("STATIC_SERVICE_PORT", 5003)

# Список методов и соответствующих сервисов
METHODS_TO_SERVICES = {
    "calc.summ": f"http://localhost:{CALC_SERVICE_PORT}/calc",
    "calc.sub": f"http://localhost:{CALC_SERVICE_PORT}/calc",
    "calc.mult": f"http://localhost:{CALC_SERVICE_PORT}/calc",
    "calc.div": f"http://localhost:{CALC_SERVICE_PORT}/calc",
}
