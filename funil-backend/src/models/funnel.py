from datetime import datetime
from src.models import db

class Funnel(db.Model):
    """Modelo para armazenar funis de vendas"""
    
    __tablename__ = 'funnels'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text)
    niche = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    settings = db.Column(db.JSON, default={})
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref='funnels')
    steps = db.relationship('FunnelStep', backref='funnel', lazy='dynamic', cascade='all, delete-orphan')
    checkout_configs = db.relationship('CheckoutConfig', backref='funnel', lazy='dynamic', cascade='all, delete-orphan')
    tracking_pixels = db.relationship('TrackingPixel', backref='funnel', lazy='dynamic', cascade='all, delete-orphan')
    visitors = db.relationship('Visitor', backref='funnel', lazy='dynamic')
    payments = db.relationship('Payment', backref='funnel', lazy='dynamic')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'niche': self.niche,
            'is_active': self.is_active,
            'settings': self.settings,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'steps_count': self.steps.count(),
            'active_steps_count': self.steps.filter_by(is_active=True).count()
        }
    
    def to_dict_with_steps(self):
        """Converte o modelo para dicionário incluindo as etapas"""
        data = self.to_dict()
        data['steps'] = [step.to_dict() for step in self.steps.order_by('order_index').all()]
        return data
    
    def get_step_by_slug(self, slug):
        """Retorna uma etapa específica pelo slug"""
        return self.steps.filter_by(slug=slug).first()
    
    def clone(self, new_name, new_slug, user_id):
        """Clona o funil com um novo nome e slug"""
        new_funnel = Funnel(
            name=new_name,
            slug=new_slug,
            description=f"Cópia de {self.description}" if self.description else None,
            niche=self.niche,
            settings=self.settings.copy() if self.settings else {},
            created_by=user_id
        )
        
        db.session.add(new_funnel)
        db.session.flush()  # Para obter o ID do novo funil
        
        # Clona as etapas
        for step in self.steps.all():
            new_step = step.clone(new_funnel.id)
            db.session.add(new_step)
        
        # Clona as configurações de checkout
        for checkout in self.checkout_configs.all():
            new_checkout = checkout.clone(new_funnel.id)
            db.session.add(new_checkout)
        
        # Clona os pixels de tracking
        for pixel in self.tracking_pixels.all():
            new_pixel = pixel.clone(new_funnel.id)
            db.session.add(new_pixel)
        
        return new_funnel
    
    def __repr__(self):
        return f'<Funnel {self.name}>'

