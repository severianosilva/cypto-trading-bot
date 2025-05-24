import pandas as pd
import numpy as np
from coins.base_bot import BaseBot

class ETHBot(BaseBot):
    def __init__(self, exchange_instance, bot_name, bot_config, global_config):
        super().__init__(exchange_instance, bot_name, bot_config, global_config)
        self._log(f"ETHBot inicializado com parâmetros: {self.strategy_params}")

    def execute_strategy(self):
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe='1h', limit=200)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['sma'] = df['close'].rolling(50).mean()
            df['upper'] = df['sma'] * 1.07
            df['lower'] = df['sma'] * 0.93

            price = df['close'].iloc[-1]
            upper = df['upper'].iloc[-1]
            lower = df['lower'].iloc[-1]

            if price <= lower:
                self._log(f"🟢 COMPRA DETECTADA | Preço: {price:.2f} | Lower: {lower:.2f}")
            elif price >= upper:
                self._log(f"🔴 VENDA DETECTADA | Preço: {price:.2f} | Upper: {upper:.2f}")
            else:
                self._log(f"⚪ NEUTRO | Preço: {price:.2f} | SMA: {df['sma'].iloc[-1]:.2f}")
        except Exception as e:
            self._log(f"❌ Erro na execução: {e}", "error")
            time.sleep(60)
