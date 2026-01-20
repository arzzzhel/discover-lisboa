# Discover Lisboa - Guia Turístico Interativo

Projeto académico de Programação Web - Licenciatura em Engenharia Informática

## Descrição

Aplicação web full-stack que serve como guia turístico e gastronómico interativo da cidade de Lisboa.

## Tecnologias

- **Backend**: Python, Flask
- **Base de dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Mapas**: Leaflet.js + OpenStreetMap
- **Geocodificação**: Nominatim API
- **Email**: SMTP (Gmail)

## Funcionalidades

- Sistema de autenticação com validação por email
- Gestão de conteúdos turísticos e gastronómicos
- Mapa interativo com marcadores
- Pesquisa inteligente de locais
- Upload de multimédia (imagens, vídeos, áudio)
- Dashboard para gestão de conteúdos

## Instalação

### 1. Requisitos

- Python 3.8 ou superior
- pip (gestor de pacotes Python)

### 2. Instalar dependências

Na linha de comandos, executa:

```bash
# Windows
pip install -r requirements.txt

# macOS/Linux
pip3 install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

Criar ficheiro `.env` na raiz do projeto:

```
SECRET_KEY=your-secret-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
APP_URL=http://localhost:5001

⬇️

SECRET_KEY=uma-chave-bem-grande-aqui
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=discoverlisboa.app@gmail.com
SMTP_PASSWORD=ftisecqbecjfljpp

APP_URL=http://localhost:5001
```

**Nota**: Para usar Gmail SMTP, é necessário:
1. Ativar verificação em duas etapas na conta Google
2. Gerar uma "App Password" em https://myaccount.google.com/apppasswords

### 4. Inicializar a base de dados

```bash
# Windows
python init_db.py

# macOS/Linux
python3 init_db.py
```

### 5. Executar a aplicação

```bash
# Windows
python app.py

# macOS/Linux
python3 app.py
```

A aplicação estará disponível em: http://localhost:5001

## Estrutura do Projeto

```
discover-lisboa/
├── app.py                  # Aplicação principal Flask
├── config.py               # Configurações
├── init_db.py              # Script de inicialização da BD
├── requirements.txt        # Dependências Python
├── models.py               # Modelos da base de dados
├── auth.py                 # Sistema de autenticação
├── routes.py               # Rotas da aplicação
├── utils.py                # Funções auxiliares
├── static/
│   ├── css/
│   │   └── style.css       # Estilos CSS
│   ├── js/
│   │   ├── map.js          # Lógica do mapa
│   │   ├── search.js       # Pesquisa de locais
│   │   └── dashboard.js    # Dashboard
│   ├── uploads/            # Ficheiros carregados
│   └── images/             # Favicon
├── templates/
│   ├── base.html           # Template base
│   ├── index.html          # Página inicial
│   ├── register.html       # Registo
│   ├── validate.html       # Validação de email
│   ├── set_password.html   # Definir password
│   ├── login.html          # Login
│   ├── dashboard.html      # Dashboard
│   ├── content_form.html   # Formulário de conteúdos
│   └── map.html            # Mapa público
├── opcional/               # Documentação adicional
│   ├── README.md
│   └── FUNCIONALIDADES.md
└── .env

```

## Utilização

1. **Registo**: Criar conta com username e email
2. **Validação**: Clicar no link recebido por email
3. **Password**: Definir password após validação
4. **Login**: Aceder à dashboard
5. **Criar conteúdos**: Adicionar locais turísticos/gastronómicos
6. **Visualizar**: Ver conteúdos no mapa interativo



