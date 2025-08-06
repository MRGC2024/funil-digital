import os
import sys
from datetime import timedelta
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.models import db, init_db
from src.routes import auth_bp, credentials_bp, funnels_bp, checkout_bp, monitoring_bp, payments_bp, tracking_bp
from src.config import config

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Carrega as configurações da aplicação
app.config.from_object(config['development'])

# Inicializa o banco de dados
init_db(app)

# Configura JWT
jwt = JWTManager(app)

# Configura CORS
CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

# Registra os Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(credentials_bp, url_prefix="/api/credentials")
app.register_blueprint(funnels_bp, url_prefix="/api/funnels")
app.register_blueprint(checkout_bp, url_prefix="/api/checkout")
app.register_blueprint(monitoring_bp, url_prefix="/api/monitoring")
app.register_blueprint(payments_bp, url_prefix="/api/payments")
app.register_blueprint(tracking_bp, url_prefix="/api/tracking")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, "index.html")
        else:
            return "index.html not found", 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)