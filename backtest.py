import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=200):
    ohlcv = ccxt.binance().fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

def calculate_envelopes(df, window=50, displacements=[0.07, 0.11, 0.14]):
    df['sma'] = df['close'].rolling(window).mean()
    for d in displacements:
        df[f'upper_{int(d*100)}'] = df['sma'] * (1 + d)
        df[f'lower_{int(d*100)}'] = df['sma'] * (1 - d)
    return df

def simulate_strategy(df, initial_capital=1000):
    capital = initial_capital
    position = 0
    trades = []

    for i in range(len(df)):
        price = df.loc[i, 'close']
        sma = df.loc[i, 'sma']
        lower_7 = df.loc[i, 'lower_7']
        upper_7 = df.loc[i, 'upper_7']

        if position == 0 and price <= lower_7:
            entry_price = price
            position = capital / price
            capital = 0
            stop_loss = entry_price - abs(entry_price - sma) * 0.4
            take_profit = entry_price + (entry_price - stop_loss)
            trades.append({'timestamp': df.loc[i, 'timestamp'], 'type': 'COMPRA', 'price': entry_price})

        elif position > 0 and (price >= take_profit or price <= stop_loss):
            capital = position * price
            position = 0
            trades.append({'timestamp': df.loc[i, 'timestamp'], 'type': 'VENDA', 'price': price})

    df['portfolio_value'] = capital + position * df['close']
    df.set_index('timestamp', inplace=True)
    df['portfolio_value'].plot(title="Backtest - Envelopes Strategy")
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    df = fetch_ohlcv('BTC/USDT', '1h', 1000)
    df = calculate_envelopes(df)
    simulate_strategy(df)