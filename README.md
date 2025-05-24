# Robô Trader de Criptomoedas com Estratégia de Envelopes

Este é um robô trader simples e modularizado que opera com estratégia de **reversão à média (Mean Reversion)** usando **envelopes de média móvel**.

## Funcionalidades

- Estratégia de envelopes (7%, 11%, 14%)
- Proteção de capital (stop loss, take profit)
- Multi-moedas (BTC, ETH, SOL, XRP, DOGE – basta adicionar novos bots)
- Sistema de logs detalhados
- Controle remoto via 
- Backtest funcional com gráficos

## Como Rodar Localmente

1. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

2. Configure suas credenciais:
   ```
   cp secret.json.example secret.json
   nano secret.json
   ```

3. Rode o bot:
   ```
   python main.py
   ```

4. Faça backtest:
   ```
   python backtest.py
   ```

## Deploy no Railway

1. Conecte seu repositório ao [Railway.app](https://railway.app )
2. Configure variáveis de ambiente:
   - 
   - 
3. O arquivo  já está configurado.

## ⚠️ Segurança

NUNCA envie seu  para o GitHub. Use variáveis de ambiente em produção.

É possível rodar estratégias diferentes por moeda, e até integrar notificações (Telegram/Discord).
