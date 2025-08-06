from src.main import app
from src.models import db, migrate

# Inicializa o Flask-Migrate com a aplicação e o banco de dados
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run()

