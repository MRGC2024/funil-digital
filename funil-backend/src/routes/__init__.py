from flask import Blueprint

# Blueprints para as diferentes seções da API
auth_bp = Blueprint("auth", __name__)
credentials_bp = Blueprint("credentials", __name__)
funnels_bp = Blueprint("funnels", __name__)
checkout_bp = Blueprint("checkout", __name__)
monitoring_bp = Blueprint("monitoring", __name__)
payments_bp = Blueprint("payments", __name__)
tracking_bp = Blueprint("tracking", __name__)

# Importa as rotas para que sejam registradas nos Blueprints
from . import auth, credentials, funnels, checkout, monitoring, payments, tracking

