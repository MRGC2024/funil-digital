from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importa todos os modelos para que sejam reconhecidos pelo Alembic
    from . import user, credential, funnel, funnel_step, checkout_config, tracking_pixel, visitor, visitor_event, payment
    
    return db

