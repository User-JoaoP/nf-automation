# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv  # Adicione esta linha

load_dotenv()  # Carrega variáveis do .env

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql://admin:admin@localhost:5432/nf_automation'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():  # Garanta o contexto durante a inicialização
        from app import routes, models
        db.create_all()  # Opcional: Cria tabelas se não existirem
    
    return app