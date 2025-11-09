🛒 Projeto E-Commerce Simplificado (FastAPI + MySQL)
📘 Descrição

Aplicação web desenvolvida com FastAPI e MySQL para gerenciamento de produtos com login e cadastro de usuários.
Inclui CRUD completo, filtros por preço e categoria, e demonstração prática dos algoritmos MergeSort e Busca Binária.

O projeto foi criado como parte dos estudos da disciplina de Algoritmos e Complexidade, com ênfase na integração entre estruturas de dados, ordenação e persistência em banco de dados.

⚙️ Tecnologias Utilizadas

Backend: Python 3.11 • FastAPI • SQLAlchemy • Pydantic

Banco de Dados: MySQL

Frontend: HTML5 • CSS3 • JavaScript • Bootstrap 5

Autenticação: JWT + Hash de Senha (bcrypt)

Outros: CORS Middleware, dotenv para configurações seguras

🧩 Funcionalidades

✅ Cadastro e login de usuários
✅ CRUD de produtos
✅ Filtro por nome, categoria e preço
✅ Ordenação por preço usando MergeSort (O(n log n))
✅ Busca binária por preço (O(log n))
✅ Redirecionamento automático para a tela de login
✅ Interface web responsiva e moderna com Bootstrap

🚀 Como Executar o Projeto
1️⃣ Clonar e acessar o projeto
git clone https://github.com/fabioX69/E-commerce-Projeto.git
cd E-commerce-Projeto

2️⃣ Criar ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Configurar o banco de dados

No MySQL, crie o banco:

CREATE DATABASE ecommerce;

5️⃣ Configurar o arquivo .env

Copie o .env.example e renomeie para .env:

APP_NAME=Projeto E-commerce
DB_URL=mysql+mysqldb://root:root3333@localhost:3306/ecommerce
SECRET_KEY=sua_chave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=60

6️⃣ Rodar o servidor
python -m uvicorn app.main:app --reload


Abra no navegador:

🌍 http://127.0.0.1:8000
 → Tela de login

⚙️ http://127.0.0.1:8000/docs
 → Documentação Swagger

🧠 Estrutura de Pastas
app/
├── api/           # Rotas de autenticação e produtos
├── core/          # Configurações e segurança (JWT, bcrypt)
├── db/            # Conexão com MySQL
├── models/        # Modelos ORM (User, Product)
├── schemas/       # Validações Pydantic
├── services/      # Lógica de CRUD e algoritmos
└── static/        # Interface HTML, JS e CSS

📚 Algoritmos Aplicados
Algoritmo	Aplicação	Complexidade
MergeSort	Ordenar produtos por preço	O(n log n)
Busca Binária	Localizar produto por preço	O(log n)
Heap	Top N produtos mais caros	O(n log k)
👨‍💻 Autor

Fabio Santos Louzada Junior
📘 Estudante de Ciência da Computação
🔗 GitHub: github.com/fabioX69
