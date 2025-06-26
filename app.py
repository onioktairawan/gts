from flask import Flask
from config import MONGO_URI, DB_NAME
from models.db import init_db
from routes.auth import auth_bp
from routes.trade import trade_bp
from routes.capital import capital_bp

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# DB Setup
init_db(MONGO_URI, DB_NAME)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(trade_bp)
app.register_blueprint(capital_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
