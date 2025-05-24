import json
import os
import logging

logger = logging.getLogger(__name__)

def load_json_config(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Arquivo {file_path} não encontrado.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON em {file_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"Erro ao carregar {file_path}: {e}")
        return None

def save_json_config(file_path, data):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar {file_path}: {e}")
        return False