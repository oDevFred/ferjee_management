from app import create_app

app = create_app()

with app.app_context():
    try:
        # Verificar se o template existe
        template_list = app.jinja_env.list_templates()
        print("Templates disponíveis:")
        for template in template_list:
            print(f"  - {template}")
        
        # Tentar carregar o template específico
        try:
            template = app.jinja_env.get_template('auth/listar_usuarios.html')
            print("\n✅ Template 'auth/listar_usuarios.html' encontrado!")
        except Exception as e:
            print(f"\n❌ Erro ao carregar template: {e}")
            
    except Exception as e:
        print(f"Erro: {e}")