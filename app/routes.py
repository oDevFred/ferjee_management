from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import Aluno, Usuario, Curso, Matricula
from .forms import FormAluno
from .auth_forms import FormLogin, FormRegistro
from .curso_forms import FormCurso, FormMatricula
from sqlalchemy import func
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    print("🏠 Acessando página inicial")
    return render_template('index.html')

@bp.route('/health')
def health_check():
    print("❤️ Verificação de saúde do sistema")
    return {'status': 'ok', 'message': 'Sistema operacional'}

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
            usuario.ultimo_login = datetime.utcnow()
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
    print("📝 Acessando página de registro de usuário")
    
    if not current_user.is_admin:
        flash('Apenas administradores podem registrar novos usuários', 'danger')
        return redirect(url_for('main.index'))
    
    form = FormRegistro()
    
    if form.validate_on_submit():
        print("📝 Formulário de registro validado")
        
        usuario = Usuario(
            username=form.username.data,
            email=form.email.data,
            nome_completo=form.nome_completo.data
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
    
    if not current_user.is_admin:
        flash('Apenas administradores podem acessar esta página', 'danger')
        return redirect(url_for('main.index'))
    
    try:
        usuarios = Usuario.query.all()
        print(f"🔢 Encontrados {len(usuarios)} usuário(s) no banco de dados")
        
        return render_template('auth/listar_usuarios.html', usuarios=usuarios)
        
    except Exception as e:
        print(f"❌ Erro ao listar usuários: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Erro ao carregar página: {str(e)}", 500

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

@bp.route('/cursos')
@login_required
def listar_cursos():
    print("📚 Listando todos os cursos")
    
    try:
        cursos = Curso.query.all()
        print(f"🔢 Encontrados {len(cursos)} curso(s) no banco de dados")
        
        # Imprimir informações sobre cada curso
        for curso in cursos:
            print(f"📚 Curso: {curso.nome} (Duração: {curso.duracao_meses} meses)")
        
        return render_template('cursos/listar.html', cursos=cursos)
        
    except Exception as e:
        print(f"❌ Erro ao listar cursos: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Erro ao carregar página: {str(e)}", 500

@bp.route('/cursos/novo', methods=['GET', 'POST'])
@login_required
def novo_curso():
    print("📚 Acessando formulário de novo curso")
    
    if not current_user.is_admin:
        flash('Apenas administradores podem criar novos cursos', 'danger')
        return redirect(url_for('main.listar_cursos'))
    
    form = FormCurso()
    
    if form.validate_on_submit():
        print("📝 Formulário de curso validado com sucesso!")
        print(f"📚 Dados do curso: {form.nome.data}")
        
        # Criar novo curso
        curso = Curso(
            nome=form.nome.data,
            descricao=form.descricao.data,
            duracao_meses=form.duracao_meses.data,
            valor_mensalidade=form.valor_mensalidade.data,
            ativo=form.ativo.data
        )
        
        # Adicionar ao banco de dados
        print("💾 Salvando curso no banco de dados...")
        db.session.add(curso)
        db.session.commit()
        print("✅ Curso salvo com sucesso!")
        
        flash('Curso criado com sucesso!', 'success')
        return redirect(url_for('main.listar_cursos'))
    
    if request.method == 'POST':
        print("❌ Formulário com erros de validação")
        for field, errors in form.errors.items():
            print(f"⚠️ Erro no campo '{field}': {errors}")
    
    return render_template('cursos/novo.html', form=form)

@bp.route('/matriculas')
@login_required
def listar_matriculas():
    print("📝 Listando todas as matrículas")
    
    try:
        matriculas = Matricula.query.all()
        print(f"🔢 Encontradas {len(matriculas)} matrícula(s) no banco de dados")
        
        return render_template('matriculas/listar.html', matriculas=matriculas)
        
    except Exception as e:
        print(f"❌ Erro ao listar matrículas: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Erro ao carregar página: {str(e)}", 500

@bp.route('/matriculas/nova', methods=['GET', 'POST'])
@login_required
def nova_matricula():
    print("📝 Acessando formulário de nova matrícula")
    
    form = FormMatricula()
    
    # Preencher as opções do select
    form.aluno_id.choices = [(a.id, f"{a.nome} ({a.matricula})") for a in Aluno.query.filter_by(ativo=True).all()]
    form.curso_id.choices = [(c.id, c.nome) for c in Curso.query.filter_by(ativo=True).all()]
    
    if form.validate_on_submit():
        print("📝 Formulário de matrícula validado com sucesso!")
        
        # Verificar se o aluno já está matriculado neste curso
        matricula_existente = Matricula.query.filter_by(
            aluno_id=form.aluno_id.data,
            curso_id=form.curso_id.data,
            status='ativo'
        ).first()
        
        if matricula_existente:
            flash('Este aluno já está matriculado neste curso!', 'danger')
            return render_template('matriculas/nova.html', form=form)
        
        # Criar nova matrícula
        matricula = Matricula(
            aluno_id=form.aluno_id.data,
            curso_id=form.curso_id.data,
            status=form.status.data,
            observacoes=form.observacoes.data
        )
        
        # Adicionar ao banco de dados
        print("💾 Salvando matrícula no banco de dados...")
        db.session.add(matricula)
        db.session.commit()
        print("✅ Matrícula salva com sucesso!")
        
        flash('Matrícula realizada com sucesso!', 'success')
        return redirect(url_for('main.listar_matriculas'))
    
    if request.method == 'POST':
        print("❌ Formulário com erros de validação")
        for field, errors in form.errors.items():
            print(f"⚠️ Erro no campo '{field}': {errors}")
    
    return render_template('matriculas/nova.html', form=form)

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
        
        # Total de cursos
        total_cursos = Curso.query.count()
        print(f"📚 Total de cursos: {total_cursos}")
        
        # Total de matrículas
        total_matriculas = Matricula.query.count()
        print(f"📝 Total de matrículas: {total_matriculas}")
        
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
            total_cursos=total_cursos,
            total_matriculas=total_matriculas,
            alunos_por_estado=alunos_por_estado,
            alunos_por_mes=alunos_por_mes
        )
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatórios: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Erro ao gerar relatórios: {str(e)}", 500

# ... (manter as outras rotas existentes)