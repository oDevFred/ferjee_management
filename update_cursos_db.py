from app import create_app, db
from app.models import Curso, Matricula
from datetime import datetime

app = create_app()

with app.app_context():
    print("🔄 Atualizando banco de dados com tabelas de cursos e matrículas...")
    
    # Criar as tabelas
    db.create_all()
    print("✅ Tabelas criadas com sucesso!")
    
    # Verificar se já existem cursos de exemplo
    if Curso.query.count() == 0:
        print("📚 Criando cursos de exemplo...")
        
        cursos = [
            {
                'nome': 'Jiu-Jitsu Básico',
                'descricao': 'Curso introdutório de Jiu-Jitsu para iniciantes',
                'duracao_meses': 6,
                'valor_mensalidade': 150.00
            },
            {
                'nome': 'Jiu-Jitsu Intermediário',
                'descricao': 'Curso para alunos com faixa branca e cinza',
                'duracao_meses': 12,
                'valor_mensalidade': 200.00
            },
            {
                'nome': 'Jiu-Jitsu Avançado',
                'descricao': 'Curso para alunos com faixa roxa e marrom',
                'duracao_meses': 18,
                'valor_mensalidade': 250.00
            },
            {
                'nome': 'Defesa Pessoal',
                'descricao': 'Curso de defesa pessoal com técnicas de Jiu-Jitsu',
                'duracao_meses': 3,
                'valor_mensalidade': 180.00
            }
        ]
        
        for curso_data in cursos:
            curso = Curso(**curso_data)
            db.session.add(curso)
        
        db.session.commit()
        print("✅ Cursos de exemplo criados!")
    else:
        print("ℹ️ Cursos já existem no banco de dados")
    
    print("🎉 Atualização do banco de dados concluída!")