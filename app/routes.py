from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import Aluno
from .forms import FormAluno

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    print("🏠 Acessando página inicial")
    return render_template('index.html')

@bp.route('/health')
def health_check():
    print("❤️ Verificação de saúde do sistema")
    return {'status': 'ok', 'message': 'Sistema operacional'}

@bp.route('/alunos')
def listar_alunos():
    print("📋 Listando todos os alunos")
    alunos = Aluno.query.all()
    print(f"🔢 Encontrados {len(alunos)} aluno(s) no banco de dados")
    return render_template('alunos/listar.html', alunos=alunos)

@bp.route('/alunos/novo', methods=['GET', 'POST'])
def novo_aluno():
    print("➕ Acessando formulário de novo aluno")
    form = FormAluno()
    
    if form.validate_on_submit():
        print("📝 Formulário validado com sucesso!")
        print(f"👤 Dados do aluno: {form.nome.data}")
        
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
        print("💾 Salvando aluno no banco de dados...")
        db.session.add(aluno)
        db.session.commit()
        print("✅ Aluno salvo com sucesso!")
        
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('main.listar_alunos'))
    
    if request.method == 'POST':
        print("❌ Formulário com erros de validação")
        for field, errors in form.errors.items():
            print(f"⚠️ Erro no campo '{field}': {errors}")
    
    return render_template('alunos/novo.html', form=form)