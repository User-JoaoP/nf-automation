from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired, Email

class FornecedorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    prazo = DateField('Prazo', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Salvar')