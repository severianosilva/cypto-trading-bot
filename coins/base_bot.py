import os
import time
import logging
from threading import Thread

logger = logging.getLogger(__name__)

class BaseBot(Thread):
    def __init__(self, exchange_instance, bot_name, bot_config, global_config):
        super().__init__(daemon=True)
        self.exchange = exchange_instance
        self.bot_name = bot_name
        self.bot_config = bot_config
        self.global_config = global_config
        self.symbol = bot_config['symbol']
        self.strategy_params = bot_config.get('strategy_params', {})
        self.loop_delay = bot_config.get('loop_delay_seconds', 60)
        self.is_running = True
        self.state_file = os.path.join(global_config.get('state_dir', 'states'), f"{bot_name}_state.json")
        self.control_file = global_config.get('control_file', 'control.json')
        self._load_state()

    def _load_state(self):
        from utils.config_loader import load_json_config
        state = load_json_config(self.state_file)
        self.state = state or {}

    def run(self):
        while self.is_running:
            try:
                self.execute_strategy()
                time.sleep(self.loop_delay)
            except Exception as e:
                logger.error(f"[{self.bot_name}] Erro na estratégia: {e}", exc_info=True)
                time.sleep(self.loop_delay * 2)

    def execute_strategy(self):
        raise NotImplementedError("execute_strategy() deve ser implementado nas subclasses.")

    def stop_bot(self):
        self.is_running = False
        logger.info(f"[{self.bot_name}] Bot interrompido.")

    def _log(self, message, level="info"):
        log_method = getattr(logger, level, logger.info)
        log_method(f"[{self.bot_name}] {message}")

    def _save_state(self):
        from utils.config_loader import save_json_config
        save_json_config(self.state_file, self.state)
