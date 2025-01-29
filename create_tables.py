from app import create_app, db
from app.models import Fornecedor

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")