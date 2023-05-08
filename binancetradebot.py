#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Binance API keys and cryptocurrency to buy
api_key = ''
secret_key = ''
symbol = 'ETH/BUSD'

# Bakiyeyi ve fiyatları al
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': secret_key
})
balance = exchange.fetch_balance()

# Get balance and prices
def trade(symbol, side, amount):
    try:
        exchange.create_order(symbol, type='market', side=side, amount=amount)
    except ccxt.InsufficientFunds:
        print('insufficient balance')
        return

# Trend tracking with Hull moving average
def get_hull_trend(symbol, interval, window):
    candles = exchange.fetch_ohlcv(symbol, interval)
    close_prices = np.asarray([x[4] for x in candles], dtype='float')
    hull = ta.WMA(ta.WMA(close_prices, int(window/2)), int(np.sqrt(window)))
    return hull

# Bot start working

while True:
    # 50-day Hull moving average
    hull = get_hull_trend(symbol, '4h', 50)

    # Get last Hull value
    last_hull = hull[-1]

    # Get current price
    ticker = exchange.fetch_ticker(symbol)
    price = ticker['last']

    # Sell if Hull is below the moving average
    if price < last_hull:
        trade(symbol, 'sell', balance['ETH']['free'])
        print("Satıldı:", price)

    # If Hull is above the moving average, buy
    elif price > last_hull:
        # Set 2% stop loss
        stop_loss = price * 0.98
        amount = balance['BUSD']['free'] / price
        trade(symbol, 'buy', amount)
        print("Alındı:", price)

    # Run every 5 minutes
    time.sleep(300)





