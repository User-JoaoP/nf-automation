from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import Fornecedor
from app import db

def init_routes(app):
    @app.route('/')
    def index():
        try:
            fornecedores = Fornecedor.query.all()
            return render_template('index.html', fornecedores=fornecedores)
        except Exception as e:
            flash(f"Erro ao carregar fornecedores: {str(e)}", "danger")
            return render_template('index.html', fornecedores=[])

    @app.route('/adicionar', methods=['GET', 'POST'])
    def adicionar_fornecedor():
        if request.method == 'POST':
            try:
                nome = request.form['nome']
                email = request.form['email']
                prazo_str = request.form['prazo']
                
                prazo = datetime.strptime(prazo_str, '%Y-%m-%d').date()
                
                novo_fornecedor = Fornecedor(
                    nome=nome, 
                    email=email, 
                    prazo=prazo, 
                    status='pendente'
                )
                
                db.session.add(novo_fornecedor)
                db.session.commit()
                
                flash('Fornecedor adicionado com sucesso!', 'success')
                return redirect(url_for('index'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao adicionar fornecedor: {str(e)}', 'danger')
        
        return render_template('add_fornecedor.html')