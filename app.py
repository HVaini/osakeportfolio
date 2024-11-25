from flask import Flask, redirect, render_template, request, session
from os import getenv
import psycopg2
from psycopg2 import extras
from werkzeug.security import check_password_hash, generate_password_hash

# lisää .env tiedostoon alla olevat (oma SECRET_KEY kurssimateriaalin ohjeiden mukaan sekä oma tietokanta DATABASE_URL)
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")  
app.config["SESSION_PERMANENT"] = False  

# yhdistys tietokantaan
DATABASE_URL = getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, cursor_factory=extras.DictCursor)

@app.route("/")
def index():
    if "username" in session:
        return redirect("/portfolios")
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and check_password_hash(user["password_hash"], password):
        session["username"] = username
        session["user_id"] = user["id"]
        return redirect("/portfolios")
    else:
        return render_template("index.html", error="Virheellinen käyttäjätunnus tai salasana")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    hashed_password = generate_password_hash(password)

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password),
        )
        conn.commit()
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
    
    # Hae portfolioon lisätyt osakkeet
    cursor.execute("""
        SELECT s.id, s.symbol, s.name, ps.quantity, s.price, 
               (ps.quantity * s.price) AS total_value
        FROM portfolio_stocks ps
        JOIN stocks s ON ps.stock_id = s.id
        WHERE ps.portfolio_id = %s
    """, (portfolio_id,))
    stocks = cursor.fetchall()

    # kaikki tietokannan osakkeet valikkoon
    cursor.execute("SELECT id, symbol, name FROM stocks")
    all_stocks = cursor.fetchall()
    cursor.close()

    return render_template("portfolio.html", portfolio=portfolio, stocks=stocks, all_stocks=all_stocks)


@app.route("/add_stock_to_portfolio", methods=["POST"])
def add_stock_to_portfolio():
    
    portfolio_id = request.form.get("portfolio_id")
    stock_id = request.form.get("stock_id")
    quantity = request.form.get("quantity")

    print("Portfolio ID:", portfolio_id)
    print("Stock ID:", stock_id)
    print("Quantity:", quantity)
    print("Lomakkeelta saatu portfolio_id:", portfolio_id)	
    
    if not portfolio_id or not stock_id or not quantity:
        return "Kaikkia kenttiä ei ole täytetty" 

    #try:
        #quantity = int(quantity)  
    #except ValueError:
        #return "Määrän täytyy olla numero"

    # Lisää osake portfolioon
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO portfolio_stocks (portfolio_id, stock_id, quantity)
            VALUES (%s, %s, %s)
            
            ON CONFLICT (portfolio_id, stock_id)
            DO UPDATE SET quantity = portfolio_stocks.quantity + EXCLUDED.quantity
            """,
            (portfolio_id, stock_id, quantity),
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
    cursor.close()

    return render_template("stocks.html", stocks=stocks, order_by=order_by, order_direction=order_direction)

