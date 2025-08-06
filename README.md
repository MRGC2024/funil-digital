# 🚀 Funil Digital - Sistema Completo de Gerenciamento de Funis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://www.postgresql.org/)

## 📋 Sobre o Projeto

O **Funil Digital** é uma aplicação completa para criação, gerenciamento e otimização de funis de vendas digitais. Desenvolvido com tecnologias modernas, oferece uma interface intuitiva para marketers e empresários gerenciarem seus funis de conversão de forma eficiente.

### 🎯 Principais Funcionalidades

- ✅ **Dashboard Administrativo Completo**
- ✅ **Gerenciamento de Credenciais de Integração**
- ✅ **Sistema Modular de Funis**
- ✅ **Checkout Customizável**
- ✅ **Monitoramento em Tempo Real**
- ✅ **Sistema de Tracking (Facebook, Google, TikTok)**
- ✅ **Autenticação Segura com JWT**
- ✅ **Interface Responsiva e Moderna**
- ✅ **API REST Completa**
- ✅ **Relatórios e Analytics Avançados**

## 🏗️ Arquitetura

### Backend
- **Framework**: Flask (Python)
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticação**: JWT
- **Migrações**: Alembic

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **HTTP Client**: Fetch API

### Infraestrutura
- **Web Server**: Nginx
- **WSGI**: Gunicorn
- **SSL**: Let's Encrypt
- **Backup**: PostgreSQL + Scripts automatizados

## 📁 Estrutura do Projeto

```
funil-digital/
├── funil-backend/              # API Flask
│   ├── src/
│   │   ├── models/            # Modelos do banco de dados
│   │   │   ├── __init__.py
│   │   │   ├── user.py        # Modelo de usuários
│   │   │   ├── credential.py  # Credenciais de integração
│   │   │   ├── funnel.py      # Funis
│   │   │   ├── funnel_step.py # Etapas dos funis
│   │   │   ├── checkout_config.py # Configurações de checkout
│   │   │   ├── tracking_pixel.py  # Pixels de tracking
│   │   │   ├── visitor.py     # Visitantes
│   │   │   ├── visitor_event.py   # Eventos de visitantes
│   │   │   └── payment.py     # Pagamentos
│   │   ├── routes/            # Rotas da API
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # Autenticação
│   │   │   ├── credentials.py # Gerenciamento de credenciais
│   │   │   ├── funnels.py     # Gerenciamento de funis
│   │   │   ├── checkout.py    # Configuração de checkout
│   │   │   ├── monitoring.py  # Monitoramento
│   │   │   ├── payments.py    # Pagamentos
│   │   │   └── tracking.py    # Tracking
│   │   ├── config.py          # Configurações
│   │   └── main.py           # Aplicação principal
│   ├── migrations/           # Migrações do banco
│   ├── venv/                # Ambiente virtual
│   ├── app.py               # Ponto de entrada
│   ├── .env                 # Variáveis de ambiente
│   └── requirements.txt     # Dependências Python
├── funil-frontend/          # Interface React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/          # Hooks personalizados
│   │   │   └── useAuth.js  # Hook de autenticação
│   │   ├── services/       # Serviços de API
│   │   │   └── api.js      # Cliente da API
│   │   ├── App.jsx         # Componente principal
│   │   └── main.jsx        # Ponto de entrada
│   ├── public/             # Arquivos estáticos
│   ├── package.json        # Dependências Node.js
│   └── vite.config.js      # Configuração do Vite
├── docs/                   # Documentação
│   ├── MANUAL_INSTALACAO.md
│   ├── MANUAL_USUARIO.md
│   └── API_DOCS.md
└── README.md              # Este arquivo
```

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Git

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/funil-digital.git
cd funil-digital
```

### 2. Configure o Backend

```bash
cd funil-backend

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar banco de dados
sudo -u postgres psql
CREATE USER funil_user WITH PASSWORD 'funil_password';
CREATE DATABASE funil_db OWNER funil_user;
GRANT ALL PRIVILEGES ON DATABASE funil_db TO funil_user;
\q

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# Executar migrações
export FLASK_APP=app.py
flask db upgrade

# Criar usuário admin
python -c "
from src.models.user import User
from src.models import db
from werkzeug.security import generate_password_hash
from src.main import app

with app.app_context():
    admin = User(
        name='Administrador',
        email='admin@funil.com',
        password_hash=generate_password_hash('123456'),
        role='admin',
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    print('Usuário admin criado!')
"

# Iniciar servidor
python app.py
```

### 3. Configure o Frontend

```bash
cd ../funil-frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

### 4. Acesse a Aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Login**: admin@funil.com / 123456

## 📚 Documentação

### Manuais Disponíveis

- 📖 **[Manual de Instalação](MANUAL_INSTALACAO.md)**: Guia completo de instalação e deploy
- 👤 **[Manual do Usuário](MANUAL_USUARIO.md)**: Como usar todas as funcionalidades
- 🔧 **[Documentação da API](API_DOCS.md)**: Referência completa da API REST

### Recursos Adicionais

- 🎥 **Vídeos Tutoriais**: [YouTube Channel](https://youtube.com/funil-digital)
- 💬 **Comunidade**: [Discord Server](https://discord.gg/funil-digital)
- 📧 **Suporte**: suporte@funil-digital.com

## 🛠️ Desenvolvimento

### Configuração do Ambiente de Desenvolvimento

```bash
# Backend
cd funil-backend
source venv/bin/activate
pip install -r requirements.txt
export FLASK_ENV=development
python app.py

# Frontend
cd funil-frontend
npm install
npm run dev
```

### Executando Testes

```bash
# Backend
cd funil-backend
python -m pytest tests/

# Frontend
cd funil-frontend
npm run test
```

### Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🚀 Deploy em Produção

### Deploy Automatizado

```bash
# Clone o repositório no servidor
git clone https://github.com/seu-usuario/funil-digital.git
cd funil-digital

# Execute o script de deploy
chmod +x deploy.sh
./deploy.sh
```

### Deploy Manual

Consulte o [Manual de Instalação](MANUAL_INSTALACAO.md) para instruções detalhadas de deploy em produção.

## 📊 Funcionalidades Detalhadas

### Dashboard Administrativo
- Métricas em tempo real
- Gráficos de conversão
- Status dos funis
- Visitantes ativos

### Gerenciamento de Funis
- Criação de funis modulares
- Editor visual de etapas
- Clonagem de funis
- Testes A/B

### Sistema de Credenciais
- Integração com gateways de pagamento
- Conexão com ferramentas de email marketing
- APIs de SMS e WhatsApp
- Pixels de tracking

### Checkout Customizável
- Editor visual
- Múltiplos métodos de pagamento
- Upsells e downsells
- Campos personalizáveis

### Monitoramento em Tempo Real
- Visitantes ativos
- Jornada do usuário
- Eventos de conversão
- Alertas automáticos

### Sistema de Tracking
- Facebook Pixel
- Google Analytics
- TikTok Pixel
- Eventos personalizados

## 🔧 Configurações Avançadas

### Variáveis de Ambiente

```bash
# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost/db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
FLASK_ENV=production
CORS_ORIGINS=https://yourdomain.com

# Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Configuração de Proxy Reverso (Nginx)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /var/www/funil-frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📈 Performance e Otimização

### Métricas de Performance
- **Tempo de Carregamento**: < 2 segundos
- **First Contentful Paint**: < 1.5 segundos
- **Largest Contentful Paint**: < 2.5 segundos
- **Cumulative Layout Shift**: < 0.1

### Otimizações Implementadas
- Lazy loading de componentes
- Compressão de assets
- Cache de API
- Otimização de imagens
- Minificação de CSS/JS

## 🔒 Segurança

### Medidas de Segurança Implementadas
- Autenticação JWT
- Criptografia de credenciais
- Validação de entrada
- Proteção CSRF
- Headers de segurança
- Rate limiting

### Conformidade
- LGPD (Lei Geral de Proteção de Dados)
- GDPR (General Data Protection Regulation)
- PCI DSS (para pagamentos)

## 🐛 Solução de Problemas

### Problemas Comuns

#### Backend não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar banco de dados
psql -h localhost -U funil_user -d funil_db

# Verificar logs
tail -f logs/app.log
```

#### Frontend não carrega
```bash
# Limpar cache
rm -rf node_modules package-lock.json
npm install

# Verificar porta
lsof -i :5173
```

#### Erro de CORS
- Verificar configuração de CORS_ORIGINS no backend
- Verificar URL da API no frontend

## 📞 Suporte

### Canais de Suporte
- 📧 **Email**: suporte@funil-digital.com
- 💬 **Chat**: Disponível no sistema
- 📱 **WhatsApp**: (11) 99999-9999
- 🎫 **Tickets**: sistema.funil-digital.com/support

### Horários de Atendimento
- **Segunda a Sexta**: 8h às 18h (BRT)
- **Sábado**: 9h às 15h (BRT)
- **Domingo**: Chat online apenas

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Contribuidores

- **Desenvolvedor Principal**: [Seu Nome](https://github.com/seu-usuario)
- **UI/UX Designer**: [Nome do Designer](https://github.com/designer)
- **DevOps**: [Nome do DevOps](https://github.com/devops)

## 🙏 Agradecimentos

- [Flask](https://flask.palletsprojects.com/) - Framework web Python
- [React](https://reactjs.org/) - Biblioteca JavaScript
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS
- [PostgreSQL](https://www.postgresql.org/) - Banco de dados
- [Vite](https://vitejs.dev/) - Build tool

## 📊 Status do Projeto

- ✅ **MVP Completo**: Todas as funcionalidades básicas implementadas
- 🔄 **Em Desenvolvimento**: Funcionalidades avançadas
- 📋 **Roadmap**: Veja nosso [roadmap público](https://github.com/seu-usuario/funil-digital/projects)

## 🔮 Roadmap

### Próximas Funcionalidades
- [ ] WebSocket para atualizações em tempo real
- [ ] Editor de páginas drag-and-drop
- [ ] Integrações com mais gateways de pagamento
- [ ] Sistema de afiliados
- [ ] App mobile
- [ ] Automações avançadas
- [ ] IA para otimização de conversão

---

**🚀 Transforme seus visitantes em clientes com o Funil Digital!**

*Desenvolvido com ❤️ para marketers e empreendedores digitais*

