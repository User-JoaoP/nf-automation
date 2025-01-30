from flask import render_template, request, redirect, url_for, flash
from datetime import datetime
from app import db
from app.models import Fornecedor

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

    # ▼▼▼ Rotas de Edição/Exclusão ▼▼▼
    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar_fornecedor(id):
        fornecedor = Fornecedor.query.get_or_404(id)
        if request.method == 'POST':
            try:
                fornecedor.nome = request.form['nome']
                fornecedor.email = request.form['email']
                fornecedor.prazo = datetime.strptime(request.form['prazo'], '%Y-%m-%d').date()
                db.session.commit()
                flash('Fornecedor atualizado com sucesso!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao atualizar fornecedor: {str(e)}', 'danger')
        return render_template('editar_fornecedor.html', fornecedor=fornecedor)

    @app.route('/excluir/<int:id>')
    def excluir_fornecedor(id):
        fornecedor = Fornecedor.query.get_or_404(id)
        try:
            db.session.delete(fornecedor)
            db.session.commit()
            flash('Fornecedor excluído com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir fornecedor: {str(e)}', 'danger')
        return redirect(url_for('index'))