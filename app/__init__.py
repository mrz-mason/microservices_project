# Инициализация пакета приложения
import logging

# Настройка логирования для всех модулей
logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
