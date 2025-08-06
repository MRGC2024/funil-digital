from datetime import datetime
from src.models import db

class Credential(db.Model):
    """Modelo para armazenar credenciais de APIs externas"""
    
    __tablename__ = 'credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    service = db.Column(db.String(100), nullable=False)  # 'skalepay', 'utmify', 'dataget'
    api_key = db.Column(db.Text, nullable=False)
    api_secret = db.Column(db.Text)
    api_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='credentials')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'service': self.service,
            'api_key': self.api_key[:10] + '...' if self.api_key else None,  # Mascarar chave
            'api_secret': '***' if self.api_secret else None,  # Mascarar secret
            'api_url': self.api_url,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_full(self):
        """Converte o modelo para dicionário com dados completos (apenas para uso interno)"""
        return {
            'id': self.id,
            'name': self.name,
            'service': self.service,
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'api_url': self.api_url,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_active_by_service(service):
        """Retorna a credencial ativa para um serviço específico"""
        return Credential.query.filter_by(service=service, is_active=True).first()
    
    def __repr__(self):
        return f'<Credential {self.name} - {self.service}>'

