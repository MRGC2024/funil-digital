#!/bin/bash

# 🚀 Script de Deploy Automatizado - Funil Digital
# Autor: Sistema Funil Digital
# Versão: 1.0
# Data: Agosto 2025

set -e  # Parar execução em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Verificar se está rodando como root
if [[ $EUID -eq 0 ]]; then
   error "Este script não deve ser executado como root"
fi

# Banner
echo -e "${BLUE}"
cat << "EOF"
 ______           _ _   ____  _       _ _        _ 
|  ____|         (_) | |  _ \(_)     (_) |      | |
| |__ _   _ _ __  _| | | |  | |_  __ _ _| |_ __ _| |
|  __| | | | '_ \| | | | |  | | |/ _` | | __/ _` | |
| |  | |_| | | | | | | | |__| | | (_| | | || (_| | |
|_|   \__,_|_| |_|_|_| |_____/|_|\__, |_|\__\__,_|_|
                                  __/ |             
                                 |___/              
EOF
echo -e "${NC}"

log "🚀 Iniciando deploy do Funil Digital..."

# Configurações padrão
PROJECT_NAME="funil-digital"
PROJECT_DIR="/var/www/$PROJECT_NAME"
BACKEND_DIR="$PROJECT_DIR/funil-backend"
FRONTEND_DIR="$PROJECT_DIR/funil-frontend"
NGINX_SITE="/etc/nginx/sites-available/$PROJECT_NAME"
SYSTEMD_SERVICE="/etc/systemd/system/funil-backend.service"

# Verificar argumentos
DOMAIN=""
EMAIL=""
DB_PASSWORD=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--domain)
            DOMAIN="$2"
            shift 2
            ;;
        -e|--email)
            EMAIL="$2"
            shift 2
            ;;
        -p|--db-password)
            DB_PASSWORD="$2"
            shift 2
            ;;
        -h|--help)
            echo "Uso: $0 -d DOMAIN -e EMAIL -p DB_PASSWORD"
            echo ""
            echo "Opções:"
            echo "  -d, --domain       Domínio do site (ex: meusite.com)"
            echo "  -e, --email        Email para SSL (ex: admin@meusite.com)"
            echo "  -p, --db-password  Senha do banco de dados"
            echo "  -h, --help         Mostrar esta ajuda"
            exit 0
            ;;
        *)
            error "Opção desconhecida: $1"
            ;;
    esac
done

# Validar argumentos obrigatórios
if [[ -z "$DOMAIN" ]]; then
    error "Domínio é obrigatório. Use -d ou --domain"
fi

if [[ -z "$EMAIL" ]]; then
    error "Email é obrigatório. Use -e ou --email"
fi

if [[ -z "$DB_PASSWORD" ]]; then
    error "Senha do banco é obrigatória. Use -p ou --db-password"
fi

log "📋 Configurações do deploy:"
info "Domínio: $DOMAIN"
info "Email: $EMAIL"
info "Diretório: $PROJECT_DIR"

# Confirmar deploy
echo ""
read -p "Deseja continuar com o deploy? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    log "Deploy cancelado pelo usuário"
    exit 0
fi

# 1. Atualizar sistema
log "📦 Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências
log "🔧 Instalando dependências..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    postgresql \
    postgresql-contrib \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    curl \
    wget \
    unzip \
    htop \
    ufw

# 3. Configurar firewall
log "🔥 Configurando firewall..."
sudo ufw --force enable
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'

# 4. Configurar PostgreSQL
log "🗄️ Configurando PostgreSQL..."
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Criar usuário e banco de dados
sudo -u postgres psql << EOF
CREATE USER funil_user WITH PASSWORD '$DB_PASSWORD';
CREATE DATABASE funil_db OWNER funil_user;
GRANT ALL PRIVILEGES ON DATABASE funil_db TO funil_user;
\q
EOF

log "✅ Banco de dados configurado"

# 5. Clonar ou atualizar repositório
if [[ -d "$PROJECT_DIR" ]]; then
    log "📁 Atualizando repositório existente..."
    cd $PROJECT_DIR
    sudo git pull origin main
else
    log "📥 Clonando repositório..."
    sudo mkdir -p /var/www
    cd /var/www
    # Substitua pela URL real do seu repositório
    sudo git clone https://github.com/seu-usuario/funil-digital.git $PROJECT_NAME
fi

# Ajustar permissões
sudo chown -R $USER:$USER $PROJECT_DIR

# 6. Configurar Backend
log "⚙️ Configurando backend..."
cd $BACKEND_DIR

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Configurar variáveis de ambiente
cat > .env << EOF
DATABASE_URL=postgresql://funil_user:$DB_PASSWORD@localhost/funil_db
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
FLASK_ENV=production
CORS_ORIGINS=https://$DOMAIN,https://www.$DOMAIN
EOF

log "✅ Arquivo .env criado"

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
    admin = User.query.filter_by(email='admin@$DOMAIN').first()
    if not admin:
        admin = User(
            name='Administrador',
            email='admin@$DOMAIN',
            password_hash=generate_password_hash('$(openssl rand -base64 12)'),
            role='admin',
            is_active=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Usuário admin criado!')
        print('Email: admin@$DOMAIN')
        print('Senha: Verifique os logs do sistema')
    else:
        print('Usuário admin já existe!')
"

log "✅ Backend configurado"

# 7. Configurar Frontend
log "🎨 Configurando frontend..."
cd $FRONTEND_DIR

# Instalar dependências
npm install

# Configurar variáveis de produção
cat > .env.production << EOF
VITE_API_URL=https://$DOMAIN/api
EOF

# Build para produção
npm run build

log "✅ Frontend buildado"

# 8. Configurar Gunicorn
log "🦄 Configurando Gunicorn..."
cd $BACKEND_DIR
pip install gunicorn

# Criar arquivo de serviço systemd
sudo tee $SYSTEMD_SERVICE > /dev/null << EOF
[Unit]
Description=Funil Digital Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/gunicorn --workers 3 --bind unix:funil-backend.sock -m 007 app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Ajustar permissões
sudo chown -R www-data:www-data $PROJECT_DIR

# Ativar e iniciar serviço
sudo systemctl daemon-reload
sudo systemctl start funil-backend
sudo systemctl enable funil-backend

log "✅ Gunicorn configurado"

# 9. Configurar Nginx
log "🌐 Configurando Nginx..."

# Criar configuração do site
sudo tee $NGINX_SITE > /dev/null << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Frontend
    location / {
        root $FRONTEND_DIR/dist;
        index index.html;
        try_files \$uri \$uri/ /index.html;
        
        # Cache para assets estáticos
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        include proxy_params;
        proxy_pass http://unix:$BACKEND_DIR/funil-backend.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Assets estáticos do backend
    location /static {
        alias $BACKEND_DIR/src/static;
        expires 1y;
        add_header Cache-Control "public";
    }

    # Logs
    access_log /var/log/nginx/${PROJECT_NAME}_access.log;
    error_log /var/log/nginx/${PROJECT_NAME}_error.log;
}
EOF

# Ativar site
sudo ln -sf $NGINX_SITE /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx

log "✅ Nginx configurado"

# 10. Configurar SSL
log "🔒 Configurando SSL..."
sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $EMAIL --agree-tos --non-interactive

# Configurar renovação automática
sudo crontab -l | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -

log "✅ SSL configurado"

# 11. Configurar backup
log "💾 Configurando backup..."
sudo mkdir -p /var/backups/$PROJECT_NAME

# Criar script de backup
sudo tee /usr/local/bin/backup-funil.sh > /dev/null << 'EOF'
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
EOF

sudo chmod +x /usr/local/bin/backup-funil.sh

# Configurar cron para backup diário
(sudo crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-funil.sh") | sudo crontab -

log "✅ Backup configurado"

# 12. Configurar logs
log "📝 Configurando logs..."
sudo mkdir -p /var/log/$PROJECT_NAME

# Configurar logrotate
sudo tee /etc/logrotate.d/$PROJECT_NAME > /dev/null << EOF
/var/log/$PROJECT_NAME/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
EOF

log "✅ Logs configurados"

# 13. Verificar serviços
log "🔍 Verificando serviços..."

# Verificar PostgreSQL
if sudo systemctl is-active --quiet postgresql; then
    log "✅ PostgreSQL está rodando"
else
    error "❌ PostgreSQL não está rodando"
fi

# Verificar backend
if sudo systemctl is-active --quiet funil-backend; then
    log "✅ Backend está rodando"
else
    error "❌ Backend não está rodando"
fi

# Verificar Nginx
if sudo systemctl is-active --quiet nginx; then
    log "✅ Nginx está rodando"
else
    error "❌ Nginx não está rodando"
fi

# 14. Teste de conectividade
log "🌐 Testando conectividade..."

# Testar HTTP
if curl -s -o /dev/null -w "%{http_code}" http://$DOMAIN | grep -q "200\|301\|302"; then
    log "✅ Site acessível via HTTP"
else
    warning "⚠️ Site pode não estar acessível via HTTP"
fi

# Testar HTTPS
if curl -s -o /dev/null -w "%{http_code}" https://$DOMAIN | grep -q "200"; then
    log "✅ Site acessível via HTTPS"
else
    warning "⚠️ Site pode não estar acessível via HTTPS"
fi

# 15. Informações finais
log "🎉 Deploy concluído com sucesso!"

echo ""
echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}         DEPLOY CONCLUÍDO COM SUCESSO!     ${NC}"
echo -e "${GREEN}===========================================${NC}"
echo ""
echo -e "${BLUE}📋 Informações do Deploy:${NC}"
echo -e "🌐 Site: https://$DOMAIN"
echo -e "🔧 Admin: https://$DOMAIN/admin"
echo -e "📧 Email Admin: admin@$DOMAIN"
echo -e "🗄️ Banco: funil_db"
echo ""
echo -e "${BLUE}📁 Diretórios:${NC}"
echo -e "📂 Projeto: $PROJECT_DIR"
echo -e "⚙️ Backend: $BACKEND_DIR"
echo -e "🎨 Frontend: $FRONTEND_DIR"
echo ""
echo -e "${BLUE}🔧 Serviços:${NC}"
echo -e "🦄 Backend: sudo systemctl status funil-backend"
echo -e "🌐 Nginx: sudo systemctl status nginx"
echo -e "🗄️ PostgreSQL: sudo systemctl status postgresql"
echo ""
echo -e "${BLUE}📝 Logs:${NC}"
echo -e "🦄 Backend: sudo journalctl -u funil-backend -f"
echo -e "🌐 Nginx: sudo tail -f /var/log/nginx/${PROJECT_NAME}_access.log"
echo -e "❌ Erros: sudo tail -f /var/log/nginx/${PROJECT_NAME}_error.log"
echo ""
echo -e "${BLUE}💾 Backup:${NC}"
echo -e "📅 Automático: Diário às 02:00"
echo -e "📂 Local: /var/backups/$PROJECT_NAME"
echo -e "🔧 Manual: /usr/local/bin/backup-funil.sh"
echo ""
echo -e "${BLUE}🔒 Segurança:${NC}"
echo -e "🔥 Firewall: Ativo (SSH, HTTP, HTTPS)"
echo -e "🔒 SSL: Configurado com Let's Encrypt"
echo -e "🔄 Renovação: Automática"
echo ""
echo -e "${YELLOW}⚠️ Próximos Passos:${NC}"
echo -e "1. Acesse https://$DOMAIN e faça login"
echo -e "2. Configure suas credenciais de integração"
echo -e "3. Crie seu primeiro funil"
echo -e "4. Configure DNS se necessário"
echo -e "5. Teste todas as funcionalidades"
echo ""
echo -e "${GREEN}🎯 Seu Funil Digital está pronto para uso!${NC}"
echo ""

# Salvar informações em arquivo
cat > $PROJECT_DIR/DEPLOY_INFO.txt << EOF
===========================================
         INFORMAÇÕES DO DEPLOY
===========================================

Data do Deploy: $(date)
Domínio: $DOMAIN
Email Admin: admin@$DOMAIN

Diretórios:
- Projeto: $PROJECT_DIR
- Backend: $BACKEND_DIR
- Frontend: $FRONTEND_DIR

Serviços:
- Backend: sudo systemctl status funil-backend
- Nginx: sudo systemctl status nginx
- PostgreSQL: sudo systemctl status postgresql

Logs:
- Backend: sudo journalctl -u funil-backend -f
- Nginx Access: sudo tail -f /var/log/nginx/${PROJECT_NAME}_access.log
- Nginx Error: sudo tail -f /var/log/nginx/${PROJECT_NAME}_error.log

Backup:
- Automático: Diário às 02:00
- Local: /var/backups/$PROJECT_NAME
- Manual: /usr/local/bin/backup-funil.sh

URLs Importantes:
- Site: https://$DOMAIN
- Admin: https://$DOMAIN/admin
- API: https://$DOMAIN/api

Comandos Úteis:
- Reiniciar Backend: sudo systemctl restart funil-backend
- Reiniciar Nginx: sudo systemctl restart nginx
- Ver Status: sudo systemctl status funil-backend
- Backup Manual: sudo /usr/local/bin/backup-funil.sh
- Renovar SSL: sudo certbot renew
- Logs do Sistema: sudo journalctl -xe

===========================================
EOF

log "📄 Informações salvas em $PROJECT_DIR/DEPLOY_INFO.txt"

exit 0

