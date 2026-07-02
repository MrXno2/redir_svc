import logging
from logging.handlers import RotatingFileHandler
import sys
from logging import Logger


def setup_logger(name: str = "app", level: str = "INFO") -> Logger:
    """Настройка логгера с подробным выводом"""
    
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Удаляем старые handlers если есть
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Создаем форматтер с файлом и строкой
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Вывод в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Опционально: вывод в файл
    file_handler = RotatingFileHandler(
        filename='app.log',
        maxBytes=10_485_760,  # 10 MB
        backupCount=5,        # 5 файлов
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


# Создаем глобальный логгер
logger = setup_logger()