from app import create_app

print("🚀 Iniciando servidor de desenvolvimento...")
app = create_app()

if __name__ == '__main__':
    print("🌐 Servidor rodando em http://127.0.0.1:5000")
    print("⚠️  Este é um servidor de desenvolvimento. Não use em produção!")
    app.run(debug=True)