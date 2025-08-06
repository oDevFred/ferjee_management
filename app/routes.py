from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
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
    form_novo = FormAluno()
    return render_template('alunos/listar.html', alunos=alunos, form_novo=form_novo)

@bp.route('/alunos/<int:id>/dados')
def get_aluno_dados(id):
    print(f"📤 Buscando dados do aluno ID: {id}")
    aluno = Aluno.query.get_or_404(id)
    
    # Formatar data para o formato YYYY-MM-DD
    data_nascimento = aluno.data_nascimento.strftime('%Y-%m-%d') if aluno.data_nascimento else None
    
    return jsonify({
        'id': aluno.id,
        'nome': aluno.nome,
        'rg': aluno.rg,
        'cpf': aluno.cpf,
        'data_nascimento': data_nascimento,
        'email': aluno.email,
        'telefone': aluno.telefone,
        'endereco': aluno.endereco,
        'bairro': aluno.bairro,
        'cidade': aluno.cidade,
        'estado': aluno.estado,
        'cep': aluno.cep,
        'ativo': aluno.ativo
    })

@bp.route('/alunos/novo', methods=['GET', 'POST'])
def novo_aluno():
    print("➕ Processando novo aluno")
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
        
        if request.is_json:
            return jsonify({'success': True})
        
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('main.listar_alunos'))
    
    if request.method == 'POST':
        print("❌ Formulário com erros de validação")
        for field, errors in form.errors.items():
            print(f"⚠️ Erro no campo '{field}': {errors}")
        
        if request.is_json:
            return jsonify({'success': False, 'errors': form.errors})
    
    return render_template('alunos/novo.html', form=form)

@bp.route('/alunos/<int:id>/editar', methods=['GET', 'POST'])
def editar_aluno(id):
    print(f"✏️ Processando edição do aluno ID: {id}")
    aluno = Aluno.query.get_or_404(id)
    form = FormAluno(obj=aluno)
    
    if form.validate_on_submit():
        print("📝 Formulário de edição validado com sucesso!")
        print(f"👤 Atualizando dados do aluno: {form.nome.data}")
        
        # Atualizar dados do aluno
        aluno.nome = form.nome.data
        aluno.rg = form.rg.data
        aluno.cpf = form.cpf.data
        aluno.data_nascimento = form.data_nascimento.data
        aluno.email = form.email.data
        aluno.telefone = form.telefone.data
        aluno.endereco = form.endereco.data
        aluno.bairro = form.bairro.data
        aluno.cidade = form.cidade.data
        aluno.estado = form.estado.data
        aluno.cep = form.cep.data
        aluno.ativo = form.ativo.data
        
        # Salvar alterações
        print("💾 Atualizando aluno no banco de dados...")
        db.session.commit()
        print("✅ Aluno atualizado com sucesso!")
        
        if request.is_json:
            return jsonify({'success': True})
        
        flash('Aluno atualizado com sucesso!', 'success')
        return redirect(url_for('main.listar_alunos'))
    
    if request.method == 'POST':
        print("❌ Formulário de edição com erros de validação")
        for field, errors in form.errors.items():
            print(f"⚠️ Erro no campo '{field}': {errors}")
        
        if request.is_json:
            return jsonify({'success': False, 'errors': form.errors})
    
    return render_template('alunos/editar.html', form=form, aluno=aluno)

@bp.route('/alunos/<int:id>/excluir', methods=['POST'])
def excluir_aluno(id):
    print(f"🗑️ Processando exclusão do aluno ID: {id}")
    aluno = Aluno.query.get_or_404(id)
    
    # Excluir aluno
    print(f"💣 Excluindo aluno: {aluno.nome} (ID: {id})")
    db.session.delete(aluno)
    db.session.commit()
    print("✅ Aluno excluído com sucesso!")
    
    if request.is_json:
        return jsonify({'success': True})
    
    flash('Aluno excluído com sucesso!', 'success')
    return redirect(url_for('main.listar_alunos'))