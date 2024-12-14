import yfinance as yf

price_cache = {}

def initialize_prices(conn):
    global price_cache
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM stocks")
    symbols = [row["symbol"] for row in cursor.fetchall()]
    cursor.close()

    data = yf.download(tickers=" ".join(symbols), period="1d")

    try:
        forex_data = yf.Ticker("EURUSD=X").history(period="1d")
        forex_price = float(forex_data['Close'][-1]) if not forex_data.empty else None
    except Exception as e:
        print(f"Error fetching forex data: {e}")
        forex_price = None

    if not data.empty and 'Adj Close' in data.columns:
        adj_close_data = data['Adj Close']
        for symbol in symbols:
            try:
                closing_price = adj_close_data[symbol][0]
                stock = yf.Ticker(symbol)
                stock_currency = stock.info.get('currency', 'Unknown')

                if stock_currency == 'USD' and forex_price:
                    closing_price /= forex_price

                price_cache[symbol] = round(closing_price, 2) if closing_price else None
            except KeyError:
                price_cache[symbol] = None
            except Exception as e:
                print(f"Error initializing price for {symbol}: {e}")
                price_cache[symbol] = None
    else:
        for symbol in symbols:
            price_cache[symbol] = None



def get_stock_price(symbol):
    global price_cache

    if symbol in price_cache:
        return price_cache[symbol]

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        if data.empty:
            return None

        closing_price = float(data['Close'][-1])
        stock_currency = stock.info.get('currency', 'Unknown')

        if stock_currency == 'USD':
            forex_data = yf.Ticker("EURUSD=X").history(period="1d")
            if not forex_data.empty:
                forex_price = float(forex_data['Close'][-1])
                closing_price /= forex_price

        price_cache[symbol] = round(closing_price, 2)
        return price_cache[symbol]
    except Exception as e:
        print(f"Error fetching real-time price for {symbol}: {e}")
        return None