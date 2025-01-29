from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações críticas
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave_fallback_segura')  # Adicione esta linha
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'postgresql://admin:admin@localhost:5432/nf_automation'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Importação segura de rotas
    with app.app_context():
        from app.routes import init_routes
        init_routes(app)
        db.create_all()

    return app