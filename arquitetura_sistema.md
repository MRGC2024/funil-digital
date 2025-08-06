# Arquitetura do Sistema de Funil Digital

## Stack Tecnológica Definida

### Frontend
- **Framework**: React com Next.js
- **UI Library**: Tailwind CSS + ShadCN/UI
- **Estado**: Context API + useState/useEffect
- **Comunicação**: Axios para API calls
- **WebSocket**: Socket.io-client para tempo real
- **Charts**: Recharts para dashboards
- **Drag & Drop**: React Beautiful DnD para reordenação

### Backend
- **Framework**: Flask (Python)
- **Banco de Dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Autenticação**: JWT + Flask-JWT-Extended
- **WebSocket**: Flask-SocketIO
- **CORS**: Flask-CORS
- **Validação**: Marshmallow
- **Migrations**: Flask-Migrate

### Infraestrutura
- **Containerização**: Docker (opcional)
- **Proxy Reverso**: Nginx (produção)
- **SSL**: Let's Encrypt
- **Monitoramento**: Logs estruturados

## Estrutura do Banco de Dados

### Tabelas Principais

#### 1. users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. credentials
```sql
CREATE TABLE credentials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    service VARCHAR(100) NOT NULL, -- 'skalepay', 'utmify', 'dataget'
    api_key TEXT NOT NULL,
    api_secret TEXT,
    api_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. funnels
```sql
CREATE TABLE funnels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    niche VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. funnel_steps
```sql
CREATE TABLE funnel_steps (
    id SERIAL PRIMARY KEY,
    funnel_id INTEGER REFERENCES funnels(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    step_type VARCHAR(50) NOT NULL, -- 'capture', 'vsl', 'checkout', 'upsell', 'thankyou'
    order_index INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    content JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(funnel_id, slug)
);
```

#### 5. checkout_configs
```sql
CREATE TABLE checkout_configs (
    id SERIAL PRIMARY KEY,
    funnel_id INTEGER REFERENCES funnels(id) ON DELETE CASCADE,
    step_id INTEGER REFERENCES funnel_steps(id) ON DELETE CASCADE,
    product_name VARCHAR(255) NOT NULL,
    product_price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'BRL',
    payment_methods JSONB DEFAULT '["pix"]',
    fields_config JSONB DEFAULT '{}',
    design_config JSONB DEFAULT '{}',
    upsell_config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. tracking_pixels
```sql
CREATE TABLE tracking_pixels (
    id SERIAL PRIMARY KEY,
    funnel_id INTEGER REFERENCES funnels(id) ON DELETE CASCADE,
    step_id INTEGER REFERENCES funnel_steps(id),
    pixel_type VARCHAR(50) NOT NULL, -- 'facebook', 'google', 'tiktok', 'custom'
    pixel_id VARCHAR(255) NOT NULL,
    event_name VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 7. visitors
```sql
CREATE TABLE visitors (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    ip_address INET,
    user_agent TEXT,
    funnel_id INTEGER REFERENCES funnels(id),
    current_step_id INTEGER REFERENCES funnel_steps(id),
    utm_source VARCHAR(255),
    utm_medium VARCHAR(255),
    utm_campaign VARCHAR(255),
    utm_term VARCHAR(255),
    utm_content VARCHAR(255),
    first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_online BOOLEAN DEFAULT true
);
```

#### 8. visitor_events
```sql
CREATE TABLE visitor_events (
    id SERIAL PRIMARY KEY,
    visitor_id INTEGER REFERENCES visitors(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- 'page_view', 'form_submit', 'payment_init', 'payment_complete'
    step_id INTEGER REFERENCES funnel_steps(id),
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 9. payments
```sql
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    visitor_id INTEGER REFERENCES visitors(id),
    funnel_id INTEGER REFERENCES funnels(id),
    step_id INTEGER REFERENCES funnel_steps(id),
    external_id VARCHAR(255), -- ID do gateway de pagamento
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'BRL',
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'paid', 'failed', 'cancelled'
    payment_method VARCHAR(50) DEFAULT 'pix',
    customer_data JSONB DEFAULT '{}',
    gateway_response JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Endpoints

### Autenticação
- `POST /api/auth/login` - Login do usuário
- `POST /api/auth/logout` - Logout do usuário
- `GET /api/auth/me` - Dados do usuário logado

### Credenciais
- `GET /api/credentials` - Listar credenciais
- `POST /api/credentials` - Criar credencial
- `PUT /api/credentials/{id}` - Atualizar credencial
- `DELETE /api/credentials/{id}` - Deletar credencial

### Funis
- `GET /api/funnels` - Listar funis
- `POST /api/funnels` - Criar funil
- `GET /api/funnels/{id}` - Obter funil específico
- `PUT /api/funnels/{id}` - Atualizar funil
- `DELETE /api/funnels/{id}` - Deletar funil
- `POST /api/funnels/{id}/clone` - Clonar funil

### Etapas do Funil
- `GET /api/funnels/{funnel_id}/steps` - Listar etapas
- `POST /api/funnels/{funnel_id}/steps` - Criar etapa
- `PUT /api/funnels/{funnel_id}/steps/{id}` - Atualizar etapa
- `DELETE /api/funnels/{funnel_id}/steps/{id}` - Deletar etapa
- `PUT /api/funnels/{funnel_id}/steps/reorder` - Reordenar etapas

### Checkout
- `GET /api/checkout/{funnel_id}/{step_id}` - Obter configuração do checkout
- `PUT /api/checkout/{funnel_id}/{step_id}` - Atualizar configuração do checkout
- `POST /api/checkout/{funnel_id}/{step_id}/preview` - Preview do checkout

### Monitoramento
- `GET /api/visitors` - Listar visitantes online
- `GET /api/visitors/{id}/events` - Eventos de um visitante
- `GET /api/analytics/dashboard` - Dados do dashboard

### Pagamentos
- `POST /api/payments/create` - Criar pagamento
- `GET /api/payments/{id}/status` - Status do pagamento
- `POST /api/payments/webhook` - Webhook de pagamento

### Tracking
- `GET /api/tracking/pixels` - Listar pixels
- `POST /api/tracking/pixels` - Criar pixel
- `PUT /api/tracking/pixels/{id}` - Atualizar pixel
- `DELETE /api/tracking/pixels/{id}` - Deletar pixel

## WebSocket Events

### Cliente → Servidor
- `join_funnel` - Entrar no monitoramento de um funil
- `leave_funnel` - Sair do monitoramento de um funil

### Servidor → Cliente
- `visitor_online` - Novo visitante online
- `visitor_offline` - Visitante saiu
- `visitor_step_change` - Visitante mudou de etapa
- `new_payment` - Novo pagamento recebido
- `payment_status_change` - Status de pagamento alterado

## Estrutura de Pastas

```
funil-digital/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── config.py
│   ├── migrations/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── utils/
│   │   └── styles/
│   ├── public/
│   ├── package.json
│   └── next.config.js
├── docs/
├── docker-compose.yml
└── README.md
```

