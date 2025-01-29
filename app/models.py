from app import db

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    prazo = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pendente')

    def __repr__(self):
        return f"Fornecedor('{self.nome}', '{self.email}', '{self.prazo}')"