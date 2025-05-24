import os
import time
import logging
import ccxt
from threading import Thread, RLock
from utils.logger_setup import setup_logging
from utils.config_loader import load_json_config, save_json_config

# Configuração de Logging
setup_logging(log_file_path="logs/trading_bot.log", log_level_str="INFO")
logger = logging.getLogger(__name__)

# Variável global para gerenciar os bots ativos
thread_management_lock = RLock()
active_bots_threads = {}

def initialize_exchange(config):
    """
    Inicializa a conexão com a exchange usando variáveis de ambiente ou secret.json
    """
    exchange_id = config.get('exchange_id', 'binance')
    exchange_options = config.get('exchange_options', {})

    # Primeiro tenta carregar das variáveis de ambiente (para produção)
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        # Se não encontrar variáveis de ambiente, tenta carregar do secret.json (para uso local)
        secrets = load_json_config(config['secrets_file'])
        if not secrets or exchange_id not in secrets:
            logger.critical(f"Credenciais da {exchange_id} não encontradas. Encerrando.")
            return None
        api_key = secrets[exchange_id]['apiKey']
        api_secret = secrets[exchange_id]['secret']

    try:
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'options': exchange_options,
            'enableRateLimit': True
        })

        # Teste simples de conexão
        balance = exchange.fetch_balance()
        logger.info(f"Conexão com {exchange_id} bem-sucedida.")
        logger.debug(f"Saldo disponível: {balance.get('USDT', 'Não disponível')}")
        return exchange
    except Exception as e:
        logger.error(f"Falha ao conectar com {exchange_id}: {e}", exc_info=True)
        return None


def start_bot(bot_name, bot_config, global_config, exchange_instance):
    """
    Inicia um bot individual em uma thread separada
    """
    module_path = bot_config['module_path']
    class_name = bot_config['class_name']

    try:
        module = __import__(module_path, fromlist=[class_name])
        BotClass = getattr(module, class_name)
        bot_instance = BotClass(exchange_instance, bot_name, bot_config, global_config)
        bot_instance.start()

        with thread_management_lock:
            active_bots_threads[bot_name] = {
                "thread": bot_instance,
                "config": bot_config,
                "restart_attempts": 0,
                "last_restart_time": time.time()
            }

        logger.info(f"Bot {bot_name} iniciado com sucesso.")
    except ModuleNotFoundError:
        logger.error(f"Módulo do bot {bot_name} não encontrado: {module_path}")
    except AttributeError:
        logger.error(f"Classe {class_name} não encontrada em {module_path}")
    except Exception as e:
        logger.error(f"Erro ao iniciar bot {bot_name}: {e}", exc_info=True)


def manage_bots(global_config, exchange_instance):
    """
    Gerencia o ciclo de vida dos bots com base na configuração
    """
    while True:
        current_config = load_json_config("config.json")
        bots_to_start = []

        with thread_management_lock:
            for bot_name, bot_meta_config in current_config.get("active_bots", {}).items():
                if not bot_meta_config.get("enabled", False):
                    continue
                if bot_name not in active_bots_threads or not active_bots_threads[bot_name]["thread"].is_alive():
                    bots_to_start.append((bot_name, bot_meta_config))

        for bot_name, bot_config in bots_to_start:
            logger.info(f"Iniciando bot {bot_name}")
            start_bot(bot_name, bot_config, current_config, exchange_instance)

        time.sleep(current_config.get('main_loop_delay_seconds', 60))
        logger.debug("Loop principal concluído.")


def main():
    """
    Função principal do bot
    """
    config = load_json_config("config.json")
    if not config:
        logger.critical("Falha ao carregar config.json. Encerrando.")
        return

    exchange = initialize_exchange(config)
    if not exchange:
        logger.critical("Falha ao inicializar a exchange. Encerrando.")
        return

    logger.info("🚀 Iniciando Trading Bot Avançado...")

    try:
        manage_bots(config, exchange)
    except KeyboardInterrupt:
        logger.info("Interrupção pelo usuário recebida. Encerrando...")
    except Exception as e:
        logger.critical(f"Erro crítico no loop principal: {e}", exc_info=True)
    finally:
        logger.info("Programa encerrado.")


if __name__ == '__main__':
    main()
