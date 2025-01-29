from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'postgresql://admin:admin@localhost:5432/nf_automation'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa o banco de dados
    db.init_app(app)

    # Importa as rotas DEPOIS de criar o app e o db
    with app.app_context():
        from app.routes import init_routes
        init_routes(app)  # Registra as rotas
        
        db.create_all()  # Cria tabelas se não existirem

    return app