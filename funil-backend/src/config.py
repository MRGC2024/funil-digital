import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações base da aplicação"""
    
    # Configurações Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # Configurações CORS
    CORS_ORIGINS = ["*"]  # Em produção, especificar domínios específicos
    
    # Configurações das APIs Externas
    SKALEPAY_SECRET_KEY = os.environ.get('SKALEPAY_SECRET_KEY')
    SKALEPAY_API_URL = os.environ.get('SKALEPAY_API_URL')
    
    UTMIFY_API_TOKEN = os.environ.get('UTMIFY_API_TOKEN')
    UTMIFY_API_URL = os.environ.get('UTMIFY_API_URL')
    
    DATAGET_API_TOKEN = os.environ.get('DATAGET_API_TOKEN')
    DATAGET_API_URL = os.environ.get('DATAGET_API_URL')

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

