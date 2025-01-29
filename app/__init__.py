from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Configuração do Flask e do Banco de Dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:senha_segura@localhost:5432/nf_automation')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Importe as rotas após a inicialização para evitar circular imports
from app import routes