# 🚀 Manual de Instalação e Deploy - Funil Digital

## 📋 Índice

1. [Visão Geral do Sistema](#visão-geral-do-sistema)
2. [Pré-requisitos](#pré-requisitos)
3. [Instalação Local](#instalação-local)
4. [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
5. [Configuração do Backend](#configuração-do-backend)
6. [Configuração do Frontend](#configuração-do-frontend)
7. [Deploy em Produção](#deploy-em-produção)
8. [Configurações Avançadas](#configurações-avançadas)
9. [Manutenção e Monitoramento](#manutenção-e-monitoramento)
10. [Solução de Problemas](#solução-de-problemas)

---

## 🎯 Visão Geral do Sistema

O **Funil Digital** é uma aplicação completa para gerenciamento de funis de vendas digitais, composta por:

### 🏗️ Arquitetura
- **Backend**: Flask (Python) com API REST
- **Frontend**: React com Tailwind CSS
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Comunicação**: API REST + WebSocket (futuro)

### 🔧 Funcionalidades Principais
- ✅ Dashboard administrativo completo
- ✅ Gerenciamento de credenciais de integração
- ✅ Sistema modular de funis
- ✅ Checkout customizável
- ✅ Monitoramento em tempo real
- ✅ Sistema de tracking (Facebook, Google, TikTok)
- ✅ Autenticação segura com JWT
- ✅ Interface responsiva e moderna

---

## 📋 Pré-requisitos

### 🖥️ Sistema Operacional
- **Linux**: Ubuntu 20.04+ (recomendado)
- **macOS**: 10.15+
- **Windows**: 10+ (com WSL2 recomendado)

### 🛠️ Software Necessário

#### Python e Node.js
```bash
# Python 3.11+
python3 --version

# Node.js 18+
node --version
npm --version
```

#### PostgreSQL
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# macOS (com Homebrew)
brew install postgresql

# Windows
# Baixar do site oficial: https://www.postgresql.org/download/windows/
```

#### Git
```bash
git --version
```

### 💾 Recursos Mínimos
- **RAM**: 4GB (8GB recomendado)
- **Disco**: 10GB livres
- **CPU**: 2 cores (4 cores recomendado)

---

## 🔧 Instalação Local

### 1. Clone do Repositório
```bash
# Clone o projeto (substitua pela URL real do seu repositório)
git clone https://github.com/seu-usuario/funil-digital.git
cd funil-digital

# Ou se você tem os arquivos localmente
mkdir funil-digital
cd funil-digital
# Copie os diretórios funil-backend e funil-frontend para aqui
```

### 2. Estrutura do Projeto
```
funil-digital/
├── funil-backend/          # API Flask
│   ├── src/
│   │   ├── models/         # Modelos do banco de dados
│   │   ├── routes/         # Rotas da API
│   │   └── config.py       # Configurações
│   ├── migrations/         # Migrações do banco
│   ├── venv/              # Ambiente virtual Python
│   ├── app.py             # Arquivo principal
│   ├── .env               # Variáveis de ambiente
│   └── requirements.txt   # Dependências Python
├── funil-frontend/         # Interface React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── hooks/         # Hooks personalizados
│   │   ├── services/      # Serviços de API
│   │   └── App.jsx        # Componente principal
│   ├── public/            # Arquivos estáticos
│   ├── package.json       # Dependências Node.js
│   └── vite.config.js     # Configuração do Vite
└── docs/                  # Documentação
```

---

## 🗄️ Configuração do Banco de Dados

### 1. Instalação do PostgreSQL

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### macOS
```bash
brew install postgresql
brew services start postgresql
```

### 2. Criação do Banco e Usuário
```bash
# Acesse o PostgreSQL como superusuário
sudo -u postgres psql

# No prompt do PostgreSQL, execute:
CREATE USER funil_user WITH PASSWORD 'funil_password';
CREATE DATABASE funil_db OWNER funil_user;
GRANT ALL PRIVILEGES ON DATABASE funil_db TO funil_user;
\q
```

### 3. Teste da Conexão
```bash
# Teste a conexão
psql -h localhost -U funil_user -d funil_db
# Digite a senha: funil_password
# Se conectar com sucesso, digite \q para sair
```

---

## ⚙️ Configuração do Backend

### 1. Preparação do Ambiente
```bash
cd funil-backend

# Criar ambiente virtual Python
python3 -m venv venv

# Ativar ambiente virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração das Variáveis de Ambiente
```bash
# Criar arquivo .env
cat > .env << EOF
DATABASE_URL=postgresql://funil_user:funil_password@localhost/funil_db
SECRET_KEY=sua-chave-secreta-super-segura-aqui
JWT_SECRET_KEY=outra-chave-secreta-para-jwt-aqui
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:5174
EOF
```

### 3. Inicialização do Banco de Dados
```bash
# Inicializar migrações (se não existir)
export FLASK_APP=app.py
flask db init

# Gerar migração
flask db migrate -m "Initial migration"

# Aplicar migrações
flask db upgrade
```

### 4. Criar Usuário Administrador
```bash
# Executar script para criar admin
python -c "
from src.models.user import User
from src.models import db
from werkzeug.security import generate_password_hash
from src.main import app

with app.app_context():
    admin = User.query.filter_by(email='admin@funil.com').first()
    if not admin:
        admin = User(
            name='Administrador',
            email='admin@funil.com',
            password_hash=generate_password_hash('123456'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado com sucesso!')
    else:
        print('Usuário admin já existe!')
"
```

### 5. Iniciar o Servidor Backend
```bash
# Desenvolvimento
python app.py

# O servidor estará rodando em: http://localhost:5000
```

---

## 🎨 Configuração do Frontend

### 1. Instalação das Dependências
```bash
cd funil-frontend

# Instalar dependências
npm install
# ou
pnpm install
```

### 2. Configuração da API
```bash
# Verificar se o arquivo src/services/api.js está configurado corretamente
# A URL da API deve apontar para: http://localhost:5000/api
```

### 3. Iniciar o Servidor Frontend
```bash
# Desenvolvimento
npm run dev
# ou
pnpm run dev

# O frontend estará rodando em: http://localhost:5173 ou http://localhost:5174
```

### 4. Teste da Aplicação
1. Acesse o frontend no navegador
2. Faça login com:
   - **Email**: admin@funil.com
   - **Senha**: 123456
3. Verifique se o dashboard carrega corretamente

---

## 🚀 Deploy em Produção

### 1. Preparação do Servidor

#### Requisitos do Servidor
- **VPS/Cloud**: AWS, DigitalOcean, Vultr, etc.
- **OS**: Ubuntu 20.04+ LTS
- **RAM**: 2GB mínimo (4GB recomendado)
- **Disco**: 20GB SSD
- **CPU**: 2 vCPUs

#### Configuração Inicial
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib nginx certbot python3-certbot-nginx git

# Configurar firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 2. Deploy do Backend

#### Configuração do PostgreSQL
```bash
# Configurar PostgreSQL
sudo -u postgres psql
CREATE USER funil_user WITH PASSWORD 'senha-super-segura-producao';
CREATE DATABASE funil_db OWNER funil_user;
GRANT ALL PRIVILEGES ON DATABASE funil_db TO funil_user;
\q
```

#### Deploy da Aplicação
```bash
# Clonar repositório
cd /var/www
sudo git clone https://github.com/seu-usuario/funil-digital.git
sudo chown -R $USER:$USER funil-digital
cd funil-digital/funil-backend

# Configurar ambiente virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configurar variáveis de ambiente
sudo nano .env
```

#### Arquivo .env para Produção
```bash
DATABASE_URL=postgresql://funil_user:senha-super-segura-producao@localhost/funil_db
SECRET_KEY=chave-secreta-super-complexa-para-producao
JWT_SECRET_KEY=outra-chave-secreta-jwt-para-producao
FLASK_ENV=production
CORS_ORIGINS=https://seudominio.com
```

#### Configurar Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Testar Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Criar arquivo de serviço
sudo nano /etc/systemd/system/funil-backend.service
```

#### Arquivo de Serviço Systemd
```ini
[Unit]
Description=Funil Digital Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/funil-digital/funil-backend
Environment="PATH=/var/www/funil-digital/funil-backend/venv/bin"
ExecStart=/var/www/funil-digital/funil-backend/venv/bin/gunicorn --workers 3 --bind unix:funil-backend.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl daemon-reload
sudo systemctl start funil-backend
sudo systemctl enable funil-backend
```

### 3. Deploy do Frontend

```bash
cd /var/www/funil-digital/funil-frontend

# Instalar dependências
npm install

# Configurar variáveis de produção
nano .env.production
```

#### Arquivo .env.production
```bash
VITE_API_URL=https://api.seudominio.com
```

```bash
# Build para produção
npm run build

# Mover arquivos para Nginx
sudo cp -r dist/* /var/www/html/
```

### 4. Configuração do Nginx

```bash
# Configurar Nginx
sudo nano /etc/nginx/sites-available/funil-digital
```

#### Configuração do Nginx
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    # Frontend
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        include proxy_params;
        proxy_pass http://unix:/var/www/funil-digital/funil-backend/funil-backend.sock;
    }

    # Assets estáticos
    location /static {
        alias /var/www/funil-digital/funil-backend/src/static;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/funil-digital /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Configuração SSL (HTTPS)

```bash
# Obter certificado SSL
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Testar renovação automática
sudo certbot renew --dry-run
```

---

## ⚙️ Configurações Avançadas

### 1. Configuração de Email (SMTP)

#### Backend - Adicionar ao .env
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-de-app
```

### 2. Configuração de Backup Automático

#### Script de Backup
```bash
# Criar script de backup
sudo nano /usr/local/bin/backup-funil.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/funil-digital"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump -h localhost -U funil_user funil_db > $BACKUP_DIR/db_backup_$DATE.sql

# Backup dos arquivos
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz /var/www/funil-digital

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

```bash
# Tornar executável
sudo chmod +x /usr/local/bin/backup-funil.sh

# Configurar cron para backup diário
sudo crontab -e
# Adicionar linha:
0 2 * * * /usr/local/bin/backup-funil.sh
```

### 3. Monitoramento com Logs

#### Configuração de Logs
```bash
# Criar diretório de logs
sudo mkdir -p /var/log/funil-digital

# Configurar logrotate
sudo nano /etc/logrotate.d/funil-digital
```

```bash
/var/log/funil-digital/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

---

## 🔍 Manutenção e Monitoramento

### 1. Comandos Úteis de Manutenção

#### Verificar Status dos Serviços
```bash
# Status do backend
sudo systemctl status funil-backend

# Status do PostgreSQL
sudo systemctl status postgresql

# Status do Nginx
sudo systemctl status nginx

# Logs do backend
sudo journalctl -u funil-backend -f

# Logs do Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### Reiniciar Serviços
```bash
# Reiniciar backend
sudo systemctl restart funil-backend

# Reiniciar Nginx
sudo systemctl restart nginx

# Reiniciar PostgreSQL
sudo systemctl restart postgresql
```

### 2. Atualização da Aplicação

```bash
# Fazer backup antes da atualização
/usr/local/bin/backup-funil.sh

# Atualizar código
cd /var/www/funil-digital
sudo git pull origin main

# Atualizar backend
cd funil-backend
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
sudo systemctl restart funil-backend

# Atualizar frontend
cd ../funil-frontend
npm install
npm run build
sudo cp -r dist/* /var/www/html/
```

### 3. Monitoramento de Performance

#### Instalar htop e iotop
```bash
sudo apt install htop iotop

# Monitorar recursos
htop
iotop
```

#### Monitorar Banco de Dados
```bash
# Conectar ao PostgreSQL
sudo -u postgres psql funil_db

# Verificar conexões ativas
SELECT * FROM pg_stat_activity;

# Verificar tamanho do banco
SELECT pg_size_pretty(pg_database_size('funil_db'));
```

---

## 🚨 Solução de Problemas

### 1. Problemas Comuns do Backend

#### Erro de Conexão com Banco
```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Verificar logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-*.log

# Testar conexão manual
psql -h localhost -U funil_user -d funil_db
```

#### Erro de Permissões
```bash
# Corrigir permissões dos arquivos
sudo chown -R www-data:www-data /var/www/funil-digital
sudo chmod -R 755 /var/www/funil-digital
```

#### Erro de Dependências Python
```bash
cd /var/www/funil-digital/funil-backend
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Problemas Comuns do Frontend

#### Erro de Build
```bash
cd /var/www/funil-digital/funil-frontend

# Limpar cache
rm -rf node_modules package-lock.json
npm install

# Build novamente
npm run build
```

#### Erro de CORS
- Verificar se o backend está configurado com CORS correto
- Verificar se a URL da API no frontend está correta

### 3. Problemas de Performance

#### Alto Uso de CPU
```bash
# Verificar processos
top
htop

# Otimizar Gunicorn (aumentar workers)
sudo nano /etc/systemd/system/funil-backend.service
# Alterar: --workers 3 para --workers 4
sudo systemctl daemon-reload
sudo systemctl restart funil-backend
```

#### Alto Uso de Memória
```bash
# Verificar uso de memória
free -h

# Configurar swap se necessário
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 4. Problemas de Rede

#### Nginx não Responde
```bash
# Verificar configuração
sudo nginx -t

# Verificar logs
sudo tail -f /var/log/nginx/error.log

# Reiniciar Nginx
sudo systemctl restart nginx
```

#### SSL/HTTPS Problemas
```bash
# Renovar certificado
sudo certbot renew

# Verificar certificado
sudo certbot certificates
```

---

## 📞 Suporte e Contato

### 🆘 Em Caso de Problemas

1. **Verificar Logs**: Sempre verificar os logs primeiro
2. **Documentação**: Consultar esta documentação
3. **Backup**: Fazer backup antes de mudanças importantes
4. **Testes**: Testar em ambiente de desenvolvimento primeiro

### 📧 Informações de Contato

- **Email**: suporte@funil-digital.com
- **Documentação**: https://docs.funil-digital.com
- **GitHub**: https://github.com/seu-usuario/funil-digital

---

## 📝 Notas Finais

### ✅ Checklist de Instalação Completa

- [ ] PostgreSQL instalado e configurado
- [ ] Backend rodando sem erros
- [ ] Frontend buildado e servido
- [ ] Nginx configurado corretamente
- [ ] SSL/HTTPS funcionando
- [ ] Backup automático configurado
- [ ] Monitoramento ativo
- [ ] Usuário admin criado
- [ ] Testes de funcionalidade realizados

### 🔐 Segurança

- **Senhas**: Use senhas fortes e únicas
- **Firewall**: Configure firewall adequadamente
- **SSL**: Sempre use HTTPS em produção
- **Backups**: Mantenha backups regulares e testados
- **Atualizações**: Mantenha sistema e dependências atualizados

### 📈 Performance

- **Monitoramento**: Configure monitoramento de recursos
- **Cache**: Implemente cache quando necessário
- **CDN**: Use CDN para assets estáticos
- **Otimização**: Otimize consultas de banco de dados

---

**🎉 Parabéns! Seu Funil Digital está pronto para uso!**

*Última atualização: Agosto 2025*

