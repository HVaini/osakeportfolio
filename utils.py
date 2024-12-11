import yfinance as yf

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    
    if data.empty:
        return 0.0
    
    closing_price = data['Close'][-1]

    stock_currency = stock.info.get('currency', 'Unknown')

    if stock_currency == 'USD':
        try:
            currency_pair = "EURUSD=X"
            forex_data = yf.Ticker(currency_pair)
            forex_price = forex_data.history(period="1d")['Close'][-1]
            converted_price = closing_price / forex_price
            return converted_price
        except Exception as e:
            return closing_price
    elif stock_currency == 'EUR':
        return closing_price
    else:
        return closing_price



