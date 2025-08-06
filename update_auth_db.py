from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    print("🔄 Atualizando banco de dados com tabela de usuários...")
    
    # Criar as tabelas
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
    
    # Verificar se já existe um usuário admin
    admin = Usuario.query.filter_by(username='admin').first()
    if not admin:
        print("👤 Criando usuário administrador padrão...")
        admin = Usuario(
            username='admin',
            email='admin@ferjee.org',
            nome_completo='Administrador do Sistema'
        )
        admin.set_senha('admin123')  # Senha padrão
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuário administrador criado!")
        print("🔑 Login: admin")
        print("🔑 Senha: admin123")
        print("⚠️  Por favor, altere a senha após o primeiro login!")
    else:
        print("ℹ️ Usuário administrador já existe")
    
    print("🎉 Atualização do banco de dados concluída!")