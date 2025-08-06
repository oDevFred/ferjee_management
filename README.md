# FERJEE - Sistema de Gestão de Alunos

Sistema completo para gerenciamento de alunos voltado para a FERJEE (Federação de Jiu-Jitsu Esportivo do Estado do Rio de Janeiro).

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Configuração Inicial](#configuração-inicial)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Próximos Passos](#próximos-passos)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 📖 Sobre o Projeto

Este sistema foi desenvolvido para resolver o déficit na organização e manutenção de dados relacionados aos alunos da FERJEE. Ele oferece uma interface moderna e intuitiva para gerenciar informações dos alunos, gerar relatórios e controlar o acesso de usuários.

## ✨ Funcionalidades

### 🎓 Gestão de Alunos
- Cadastro de alunos com matrícula automática (numérica de 10 dígitos)
- Edição e exclusão de alunos
- Validação de CPF em tempo real
- Armazenamento seguro de informações pessoais (nome, RG, CPF, endereço, telefone, etc.)
- Histórico de atividades/formações
- Status de ativo/inativo

### 🔐 Autenticação e Controle de Acesso
- Sistema de login para usuários autorizados
- Níveis de acesso (Administrador/Usuário)
- Apenas administradores podem criar novos usuários
- Controle de sessão com lembrar-me

### 📊 Relatórios
- Total de alunos ativos e inativos
- Distribuição de alunos por estado
- Gráficos de cadastros por mês
- Interface visual com Chart.js

### 🎨 Interface Moderna
- Design responsivo com Bootstrap 5
- Modais para operações de CRUD
- Feedback visual com emojis e mensagens
- Navegação intuitiva

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.13.5** - Linguagem principal
- **Flask** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-Login** - Gerenciamento de sessões
- **Flask-WTF** - Formulários e validação
- **SQLite** - Banco de dados (desenvolvimento)
- **Werkzeug** - Utilitários WSGI

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização
- **JavaScript** - Interações dinâmicas
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Ícones
- **Chart.js** - Gráficos para relatórios

### Outros
- **Jinja2** - Template engine
- **Git** - Controle de versão
- **Conventional Commits** - Padrão de commits

## 🚀 Instalação

### Pré-requisitos
- Python 3.13.5 ou superior
- pip (gerenciador de pacotes do Python)
- Git (para clonar o repositório)

### Passos

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/ferjee_management.git
   cd ferjee_management


2. **Crie um ambiente virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf python-dotenv email-validator werkzeug
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

## ⚙️ Configuração Inicial

1. **Inicialize o banco de dados**
   ```bash
   python update_db.py
   ```

2. **Configure o sistema de autenticação**
   ```bash
   python update_auth_db.py
   ```

3. **Inicie o servidor de desenvolvimento**
   ```bash
   flask run
   ```

4. **Acesse o sistema**
   - Abra seu navegador e acesse: http://127.0.0.1:5000
   - Faça login com as credenciais padrão:
     - Usuário: `admin`
     - Senha: `admin123`

## 📖 Uso

### Login no Sistema
1. Acesse a página inicial
2. Clique em "Fazer Login"
3. Digite suas credenciais
4. Marque "Lembrar-me" se desejar manter a sessão ativa

### Gestão de Alunos
1. No menu lateral, clique em "Alunos"
2. Para cadastrar um novo aluno:
   - Clique em "Novo Aluno"
   - Preencha os dados do formulário
   - O CPF é validado em tempo real
   - A matrícula é gerada automaticamente
3. Para editar um aluno:
   - Clique no ícone de edição (lápis)
   - Altere os dados necessários
   - Salve as alterações
4. Para excluir um aluno:
   - Clique no ícone de exclusão (lixeira)
   - Confirme a exclusão no modal

### Gestão de Usuários (Apenas Administradores)
1. No menu "Administração", clique em "Usuários"
2. Para criar um novo usuário:
   - Clique em "Novo Usuário"
   - Preencha os dados do formulário
   - O novo usuário terá acesso básico ao sistema
3. Visualize todos os usuários cadastrados
4. Veja informações como último login e tipo de acesso

### Relatórios
1. No menu lateral, clique em "Relatórios"
2. Visualize os cards com estatísticas gerais
3. Analise os gráficos de distribuição por estado
4. Veja a evolução de cadastros por mês

## 📁 Estrutura do Projeto

```
ferjee_management/
├── app/
│   ├── __init__.py          # Configuração do Flask
│   ├── models.py            # Modelos de dados
│   ├── routes.py            # Rotas da aplicação
│   ├── forms.py             # Formulários de alunos
│   ├── auth_forms.py        # Formulários de autenticação
│   ├── templates/
│   │   ├── base.html        # Template base
│   │   ├── index.html       # Página inicial
│   │   ├── alunos/
│   │   │   ├── listar.html   # Listagem de alunos
│   │   │   ├── novo.html     # Novo aluno
│   │   │   └── editar.html   # Editar aluno
│   │   ├── auth/
│   │   │   ├── login.html    # Página de login
│   │   │   ├── registrar_usuario.html  # Registrar usuário
│   │   │   └── listar_usuarios.html  # Listar usuários
│   │   └── relatorios.html   # Página de relatórios
│   └── static/              # Arquivos estáticos (CSS, JS, imagens)
├── instance/                # Banco de dados SQLite
├── venv/                    # Ambiente virtual
├── .env                     # Variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── update_db.py            # Script para atualizar o banco de dados
├── update_auth_db.py       # Script para configurar autenticação
├── check_templates.py      # Script para verificar templates
├── test_db.py              # Script para testar o banco de dados
├── init_db.py              # Script para inicializar o banco
├── run.py                   # Ponto de entrada da aplicação
└── README.md               # Documentação do projeto
```

## 📈 Próximos Passos

### 🔒 Segurança e Privacidade
1. **Implementar criptografia de dados sensíveis**
   - Criptografar CPF e RG no banco de dados
   - Implementar mascaramento de dados na interface

2. **Adicionar auditoria do sistema**
   - Registrar todas as ações dos usuários
   - Criar logs de acesso e modificações
   - Implementar página de histórico de alterações

3. **Política de senhas**
   - Implementar política de complexidade de senhas
   - Adicionar recuperação de senha
   - Implementar expiração de senhas

### 📱 Funcionalidades Adicionais
1. **Sistema de matrículas em cursos**
   - Criar modelo de Curso
   - Implementar matrícula de alunos em cursos
   - Gerar histórico de matrículas

2. **Controle de pagamentos**
   - Sistema de controle de mensalidades
   - Gerar boletos ou links de pagamento
   - Relatórios de inadimplência

3. **Sistema de presença**
   - Controle de frequência dos alunos
   - Relatórios de presença
   - Notificações de ausências

### 🎯 Melhorias na Interface
1. **Filtros e busca avançada**
   - Implementar busca por alunos
   - Filtros por status, estado, data de cadastro
   - Exportação de dados para Excel/PDF

2. **Dashboard personalizado**
   - Dashboard inicial com widgets personalizáveis
   - Gráficos interativos
   - Métricas em tempo real

3. **Modo escuro**
   - Implementar tema dark mode
   - Salvar preferências do usuário

### 🚀 Performance e Escalabilidade
1. **Otimização do banco de dados**
   - Implementar índices adicionais
   - Otimizar consultas complexas
   - Configurar cache

2. **Testes automatizados**
   - Criar testes unitários
   - Implementar testes de integração
   - Configurar CI/CD

3. **Deploy em produção**
   - Configurar servidor web (Gunicorn/uWSGI)
   - Implementar HTTPS
   - Configurar backup automático

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adicionar nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Projeto**: FERJEE - Sistema de Gestão de Alunos
- **Desenvolvedor**: oDevFred
- **Email**: caio.frederico2001@outlook.com
- **Organização**: FERJEE - Federação do Estado do Rio de Janeiro de Esportes Eletrônicos

---

> ⭐ Se este projeto foi útil para você, por favor, considere dar uma estrela no repositório!