import logging
import os

def setup_logging(log_file_path="logs/trading_bot.log", log_level_str="INFO"):
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)

    logging.basicConfig(
        level=log_level,
        handlers=[file_handler, console_handler]
    )

    logging.info("✅ Logging configurado.")