from app import create_app, db
from app.models import Fornecedor

app = create_app()  # Cria a instância do app

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso!")