from os import getenv
import psycopg2
from psycopg2 import extras
from flask import Flask
from routes import routes, init_app
from utils import initialize_prices

# lisää .env tiedostoon oma SECRET_KEY sekä oma tietokanta DATABASE_URL
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False

# yhdistys tietokantaan
DATABASE_URL = getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL, cursor_factory=extras.DictCursor)

# reittien lataus
init_app(conn)
app.register_blueprint(routes)

# Hintojen alustaminen sovelluksen käynnistyessä
initialize = True  # True esilataukselle, False reaalihinnoille(hitaampi)
if initialize:
    with app.app_context():
        initialize_prices(conn)

if __name__ == "__main__":
    app.run()
