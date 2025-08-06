from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import Aluno
from .forms import FormAluno

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/health')
def health_check():
    return {'status': 'ok', 'message': 'Sistema operacional'}

@bp.route('/alunos')
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('alunos/listar.html', alunos=alunos)

@bp.route('/alunos/novo', methods=['GET', 'POST'])
def novo_aluno():
    form = FormAluno()
    
    if form.validate_on_submit():
        # Criar novo aluno
        aluno = Aluno(
            nome=form.nome.data,
            rg=form.rg.data,
            cpf=form.cpf.data,
            data_nascimento=form.data_nascimento.data,
            email=form.email.data,
            telefone=form.telefone.data,
            endereco=form.endereco.data,
            bairro=form.bairro.data,
            cidade=form.cidade.data,
            estado=form.estado.data,
            cep=form.cep.data,
            ativo=form.ativo.data
        )
        
        # Adicionar ao banco de dados
        db.session.add(aluno)
        db.session.commit()
        
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('main.listar_alunos'))
    
    return render_template('alunos/novo.html', form=form)