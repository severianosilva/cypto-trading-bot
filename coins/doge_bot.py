import pandas as pd
import numpy as np
from coins.base_bot import BaseBot

class DOGEBot(BaseBot):
    def __init__(self, exchange_instance, bot_name, bot_config, global_config):
        super().__init__(exchange_instance, bot_name, bot_config, global_config)
        self._log(f"DOGEBot inicializado com parâmetros: {self.strategy_params}")

    def execute_strategy(self):
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.symbol, timeframe='1h', limit=200)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['sma'] = df['close'].rolling(50).mean()
            envelope_percent = self.strategy_params.get("envelope_percent", 0.15)
            df['upper'] = df['sma'] * (1 + envelope_percent)
            df['lower'] = df['sma'] * (1 - envelope_percent)

            price = df['close'].iloc[-1]
            upper = df['upper'].iloc[-1]
            lower = df['lower'].iloc[-1]

            if price <= lower:
                self._log(f"🟢 COMPRA DETECTADA | Preço: {price:.6f} | Lower: {lower:.6f}")
            elif price >= upper:
                self._log(f"🔴 VENDA DETECTADA | Preço: {price:.6f} | Upper: {upper:.6f}")
            else:
                self._log(f"⚪ NEUTRO | Preço: {price:.6f} | SMA: {df['sma'].iloc[-1]:.6f}")
        except Exception as e:
            self._log(f"❌ Erro na execução: {e}", "error")
            time.sleep(60)