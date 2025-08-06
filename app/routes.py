from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import Aluno, Usuario
from .forms import FormAluno
from .auth_forms import FormLogin, FormRegistro
from sqlalchemy import func
from datetime import datetime  # Adicionar esta importação

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    print("🏠 Acessando página inicial")
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    print("🔐 Acessando página de login")
    
    if current_user.is_authenticated:
        print(f"👤 Usuário já autenticado: {current_user.username}")
        return redirect(url_for('main.listar_alunos'))
    
    form = FormLogin()
    
    if form.validate_on_submit():
        print("📝 Formulário de login validado")
        usuario = Usuario.query.filter_by(username=form.username.data).first()
        
        if usuario and usuario.check_senha(form.senha.data):
            print(f"✅ Login bem-sucedido para o usuário: {usuario.username}")
            login_user(usuario, remember=form.lembrar_me.data)
            usuario.ultimo_login = datetime.utcnow()  # Agora funciona
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.listar_alunos'))
        else:
            print("❌ Falha no login: usuário ou senha inválidos")
            flash('Usuário ou senha inválidos', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    print(f"🚪 Usuário {current_user.username} fazendo logout")
    logout_user()
    flash('Você saiu do sistema', 'info')
    return redirect(url_for('main.login'))

@bp.route('/registrar_usuario', methods=['GET', 'POST'])
@login_required
def registrar_usuario():
    print("📝 Acessando página de registro de usuário (apenas admin)")
    
    # Verificar se o usuário atual é administrador
    if not current_user.is_admin:
        print("❌ Usuário não é administrador")
        flash('Apenas administradores podem registrar novos usuários', 'danger')
        return redirect(url_for('main.listar_alunos'))
    
    form = FormRegistro()
    
    if form.validate_on_submit():
        print("📝 Formulário de registro validado")
        
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            nome_completo=form.nome_completo.data,
            is_admin=False  # Novos usuários não são admin por padrão
        )
        usuario.set_senha(form.senha.data)
        
        db.session.add(usuario)
        db.session.commit()
        
        print(f"✅ Usuário {usuario.username} registrado com sucesso")
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('main.listar_usuarios'))
    
    return render_template('auth/registrar_usuario.html', form=form)

@bp.route('/usuarios')
@login_required
def listar_usuarios():
    print("📋 Listando todos os usuários")
    
    # Verificar se o usuário atual é administrador
    if not current_user.is_admin:
        print("❌ Usuário não é administrador")
        flash('Apenas administradores podem visualizar usuários', 'danger')
        return redirect(url_for('main.listar_alunos'))
    
    usuarios = Usuario.query.all()
    print(f"🔢 Encontrados {len(usuarios)} usuário(s) no banco de dados")
    
    return render_template('auth/listar_usuarios.html', usuarios=usuarios)

@bp.route('/alunos')
@login_required
def listar_alunos():
    print("📋 Listando todos os alunos")
    
    try:
        alunos = Aluno.query.all()
        print(f"🔢 Encontrados {len(alunos)} aluno(s) no banco de dados")
        
        # Imprimir informações sobre cada aluno
        for aluno in alunos:
            print(f"👤 Aluno: {aluno.nome} (Matrícula: {aluno.matricula})")
        
        form_novo = FormAluno()
        print("✅ Formulário criado com sucesso")
        
        print("📝 Renderizando template listar.html")
        return render_template('alunos/listar.html', alunos=alunos, form_novo=form_novo)
        
    except Exception as e:
        print(f"❌ Erro ao listar alunos: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Erro ao carregar página: {str(e)}", 500

@bp.route('/relatorios')
@login_required
def relatorios():
    print("📊 Acessando página de relatórios")
    
    try:
        # Total de alunos
        total_alunos = Aluno.query.count()
        print(f"🔢 Total de alunos: {total_alunos}")
        
        # Total de alunos ativos
        alunos_ativos = Aluno.query.filter_by(ativo=True).count()
        print(f"✅ Alunos ativos: {alunos_ativos}")
        
        # Total de alunos inativos
        alunos_inativos = Aluno.query.filter_by(ativo=False).count()
        print(f"❌ Alunos inativos: {alunos_inativos}")
        
        # Alunos por estado
        alunos_por_estado = db.session.query(
            Aluno.estado,
            func.count(Aluno.id).label('total')
        ).group_by(Aluno.estado).all()
        print("📍 Distribuição por estado:")
        for estado, total in alunos_por_estado:
            print(f"   {estado}: {total}")
        
        # Alunos por mês de cadastro
        alunos_por_mes = db.session.query(
            func.strftime('%Y-%m', Aluno.data_criacao).label('mes'),
            func.count(Aluno.id).label('total')
        ).group_by(func.strftime('%Y-%m', Aluno.data_criacao)).all()
        print("📅 Distribuição por mês:")
        for mes, total in alunos_por_mes:
            print(f"   {mes}: {total}")
        
        return render_template(
            'relatorios.html',
            total_alunos=total_alunos,
            alunos_ativos=alunos_ativos,
            alunos_inativos=alunos_inativos,
            alunos_por_estado=alunos_por_estado,
            alunos_por_mes=alunos_por_mes
        )
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatórios: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Erro ao gerar relatórios: {str(e)}", 500

@bp.route('/alunos/<int:id>/dados')
@login_required
def get_aluno_dados(id):
    print(f"📤 Buscando dados do aluno ID: {id}")
    aluno = Aluno.query.get_or_404(id)
    
    # Formatar data para o formato YYYY-MM-DD
    data_nascimento = aluno.data_nascimento.strftime('%Y-%m-%d') if aluno.data_nascimento else None
    
    return jsonify({
        'id': aluno.id,
        'matricula': aluno.matricula,
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
@login_required
def novo_aluno():
    print("➕ Processando novo aluno")
    form = FormAluno()
    
    if form.validate_on_submit():
        print("📝 Formulário validado com sucesso!")
        print(f"👤 Dados do aluno: {form.nome.data}")
        
        # Criar novo aluno (matrícula será gerada automaticamente)
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
        print(f"✅ Aluno salvo com sucesso! Matrícula gerada: {aluno.matricula}")
        
        if request.is_json:
            return jsonify({'success': True, 'matricula': aluno.matricula})
        
        flash(f'Aluno cadastrado com sucesso! Matrícula: {aluno.matricula}', 'success')
        return redirect(url_for('main.listar_alunos'))
    
    if request.method == 'POST':
        print("❌ Formulário com erros de validação")
        for field, errors in form.errors.items():
            print(f"⚠️ Erro no campo '{field}': {errors}")
        
        if request.is_json:
            return jsonify({'success': False, 'errors': form.errors})
    
    return render_template('alunos/novo.html', form=form)

@bp.route('/alunos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_aluno(id):
    print(f"✏️ Processando edição do aluno ID: {id}")
    aluno = Aluno.query.get_or_404(id)
    form = FormAluno(obj=aluno)
    
    if form.validate_on_submit():
        print("📝 Formulário de edição validado com sucesso!")
        print(f"👤 Atualizando dados do aluno: {form.nome.data} (Matrícula: {aluno.matricula})")
        
        # Atualizar dados do aluno (matrícula não pode ser alterada)
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
@login_required
def excluir_aluno(id):
    print(f"🗑️ Processando exclusão do aluno ID: {id}")
    aluno = Aluno.query.get_or_404(id)
    
    # Excluir aluno
    print(f"💣 Excluindo aluno: {aluno.nome} (Matrícula: {aluno.matricula})")
    db.session.delete(aluno)
    db.session.commit()
    print("✅ Aluno excluído com sucesso!")
    
    if request.is_json:
        return jsonify({'success': True})
    
    flash('Aluno excluído com sucesso!', 'success')
    return redirect(url_for('main.listar_alunos'))