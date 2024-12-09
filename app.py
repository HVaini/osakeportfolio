from os import getenv
from decimal import Decimal
import secrets
import psycopg2
from psycopg2 import extras
import yfinance as yf
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, redirect, render_template, request, session, flash

# lisää .env tiedostoon oma SECRET_KEY sekä oma tietokanta DATABASE_URL
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False

# yhdistys tietokantaan
DATABASE_URL = getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, cursor_factory=extras.DictCursor)

def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    return data['Close'][-1]

@app.route("/")
def index():
    if "username" in session:
        return redirect("/portfolios")
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    if not username or not password:
        return render_template("index.html", error="Käyttäjänimi ja salasana ovat pakollisia")

    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user["password_hash"], password):
        session["username"] = username
        session["user_id"] = user["id"]
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/portfolios")
    else:
        return render_template("index.html", error="Virheellinen käyttäjätunnus tai salasana")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"].strip()
    password = request.form["password"].strip()

    if not username or not password:
        return render_template("index.html", error="Käyttäjänimi ja salasana ovat pakollisia")
    
    if len(username) < 3:
        return render_template("index.html", error="Käyttäjänimen tulee olla vähintään 3 merkkiä pitkä")
    # testailun helpottamisen vuoksi salasanan minimipituus on vielä 3 merkkiä, muutetaan lopulliseen versioon
    if len(password) < 3:
        return render_template("index.html", error="Salasanan tulee olla vähintään 3 merkkiä pitkä")

    hashed_password = generate_password_hash(password)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password),
        )
        conn.commit()
        flash("Käyttäjätilin luonti onnistui. Voit nyt kirjautua sisään!")
    except psycopg2.IntegrityError:
        conn.rollback()
        return render_template("index.html", error="Käyttäjänimi on jo varattu")
    finally:
        cursor.close()

    return redirect("/")


@app.route("/portfolios")
def portfolios():
    if "username" not in session:
        return redirect("/")
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM portfolios WHERE user_id = %s", (session["user_id"],))
    user_portfolios = cursor.fetchall()
    cursor.close()

    return render_template("portfolios.html", portfolios=user_portfolios)


@app.route("/create_portfolio", methods=["POST"])
def create_portfolio():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if "username" not in session:
        return redirect("/")
    
    name = request.form["name"]

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO portfolios (user_id, name) VALUES (%s, %s)",
        (session["user_id"], name),
    )
    conn.commit()
    cursor.close()

    return redirect("/portfolios")


@app.route("/portfolio/<int:portfolio_id>")
def portfolio(portfolio_id):
    if "username" not in session:
        return redirect("/")
    
    cursor = conn.cursor()

    # Hae portfolio
    cursor.execute("SELECT id, name FROM portfolios WHERE id = %s AND user_id = %s", (portfolio_id, session["user_id"]))
    portfolio = cursor.fetchone()
    if not portfolio:
        return redirect("/portfolios")
    
    cursor.execute("""
        SELECT s.id, s.symbol, s.name, 
               SUM(t.quantity) AS total_quantity,
               SUM(t.quantity * t.purchase_price) / NULLIF(SUM(t.quantity), 0) AS average_price
        FROM stock_transactions t
        JOIN stocks s ON t.stock_id = s.id
        WHERE t.portfolio_id = %s
        GROUP BY s.id, s.symbol, s.name
    """, (portfolio_id,))
    stocks = cursor.fetchall()

    updated_stocks = []
    for stock in stocks:
        real_time_price = None
        try:
            real_time_price = get_stock_price(stock["symbol"])
        except Exception:
            pass

        real_time_price_decimal = Decimal(real_time_price) if real_time_price is not None else None
        stock_return = (
            (real_time_price_decimal - stock["average_price"]) * stock["total_quantity"]
            if real_time_price_decimal is not None and stock["average_price"] is not None
            else None
        )

        updated_stocks.append({
            "id": stock["id"],
            "symbol": stock["symbol"],
            "name": stock["name"],
            "total_quantity": stock["total_quantity"],
            "average_price": stock["average_price"],
            "real_time_price": real_time_price,
            "total_value": real_time_price * stock["total_quantity"] if real_time_price is not None else None,
            "stock_return": stock_return
        })
    
    # kaikki tietokannan osakkeet valikkoon
    cursor.execute("SELECT id, symbol, name FROM stocks")
    all_stocks = cursor.fetchall()
    cursor.close()

    return render_template(
        "portfolio.html",
        portfolio=portfolio,
        stocks=updated_stocks,
        all_stocks=all_stocks,
    )


@app.route("/add_stock_to_portfolio", methods=["POST"])
def add_stock_to_portfolio():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    portfolio_id = request.form.get("portfolio_id")
    stock_id = request.form.get("stock_id")
    quantity = request.form.get("quantity")
    purchase_price = request.form.get("purchase_price")

    if not portfolio_id or not stock_id or not quantity or not purchase_price:
        return "Kaikkia kenttiä ei ole täytetty"

    try:
        quantity = int(quantity)
        purchase_price = float(purchase_price)
        if quantity <= 0:
            return "Määrän täytyy olla vähintään 1"
        if quantity > 10**6:
            return "Määrä ei voi ylittää 1 000 000"
        if purchase_price <= 0:
            return "Oston hinnan täytyy olla positiivinen"
    except ValueError:
        return "Virheellinen määrä tai hinta"

    cursor = conn.cursor()
    try:
        # Lisää uusi osto stock_transactions-tauluun
        cursor.execute(
            """
            INSERT INTO stock_transactions (portfolio_id, stock_id, quantity, purchase_price)
            VALUES (%s, %s, %s, %s)
            """,
            (portfolio_id, stock_id, quantity, purchase_price),
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Virhe: {e}"
    finally:
        cursor.close()

    return redirect(f"/portfolio/{portfolio_id}")


@app.route("/index")
def index_alias():
    return redirect("/")


@app.route("/stocks")
def stocks():
    if "username" not in session:
        return redirect("/")
    
    order_by = request.args.get("order_by", "name")
    order_direction = request.args.get("order_direction", "asc")

    if order_by not in ["name", "symbol", "price"]:
        order_by = "name"
    if order_direction not in ["asc", "desc"]:
        order_direction = "asc"
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, symbol, name, price FROM stocks ORDER BY {order_by} {order_direction}")
    stocks = cursor.fetchall()

    stocks_with_prices = []
    for stock in stocks:
        stock_dict = dict(stock)
        try:
            stock_dict["real_time_price"] = get_stock_price(stock_dict["symbol"])
        except Exception:
            stock_dict["real_time_price"] = None
        stocks_with_prices.append(stock_dict)

    # Hae käyttäjän kaikki salkut
    cursor.execute("SELECT id, name FROM portfolios WHERE user_id = %s", (session["user_id"],))
    portfolios = cursor.fetchall()

    cursor.close()

    return render_template(
        "stocks.html", 
        stocks=stocks_with_prices, 
        order_by=order_by, 
        order_direction=order_direction, 
        portfolios=portfolios
    )

@app.route("/remove_stock", methods=["POST"])
def remove_stock():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    portfolio_id = request.form.get("portfolio_id")
    stock_id = request.form.get("stock_id")

    if not portfolio_id or not stock_id:
        return "Kaikkia kenttiä ei ole täytetty"

    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM stock_transactions
            WHERE portfolio_id = %s AND stock_id = %s
        """, (portfolio_id, stock_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return f"Virhe: {e}"
    finally:
        cursor.close()

    
    return redirect(f"/portfolio/{portfolio_id}")

