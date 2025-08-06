from datetime import datetime
from src.models import db

class FunnelStep(db.Model):
    """Modelo para armazenar etapas de um funil"""
    
    __tablename__ = 'funnel_steps'
    
    id = db.Column(db.Integer, primary_key=True)
    funnel_id = db.Column(db.Integer, db.ForeignKey('funnels.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    step_type = db.Column(db.String(50), nullable=False)  # 'capture', 'vsl', 'checkout', 'upsell', 'thankyou'
    order_index = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    settings = db.Column(db.JSON, default={})
    content = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Constraint para garantir slug único por funil
    __table_args__ = (db.UniqueConstraint('funnel_id', 'slug', name='uq_funnel_step_slug'),)
    
    # Relacionamentos
    checkout_configs = db.relationship('CheckoutConfig', backref='step', lazy='dynamic', cascade='all, delete-orphan')
    tracking_pixels = db.relationship('TrackingPixel', backref='step', lazy='dynamic', cascade='all, delete-orphan')
    visitor_events = db.relationship('VisitorEvent', lazy='dynamic')
    payments = db.relationship('Payment', backref='step', lazy='dynamic')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'funnel_id': self.funnel_id,
            'name': self.name,
            'slug': self.slug,
            'step_type': self.step_type,
            'order_index': self.order_index,
            'is_active': self.is_active,
            'settings': self.settings,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_checkout(self):
        """Converte o modelo para dicionário incluindo configuração de checkout"""
        data = self.to_dict()
        checkout = self.checkout_configs.first()
        if checkout:
            data['checkout_config'] = checkout.to_dict()
        return data
    
    def clone(self, new_funnel_id):
        """Clona a etapa para um novo funil"""
        new_step = FunnelStep(
            funnel_id=new_funnel_id,
            name=self.name,
            slug=self.slug,
            step_type=self.step_type,
            order_index=self.order_index,
            is_active=self.is_active,
            settings=self.settings.copy() if self.settings else {},
            content=self.content.copy() if self.content else {}
        )
        return new_step
    
    @staticmethod
    def reorder_steps(funnel_id, step_orders):
        """Reordena as etapas de um funil
        
        Args:
            funnel_id: ID do funil
            step_orders: Lista de dicionários com {'id': step_id, 'order_index': new_order}
        """
        for step_order in step_orders:
            step = FunnelStep.query.filter_by(
                id=step_order['id'], 
                funnel_id=funnel_id
            ).first()
            if step:
                step.order_index = step_order['order_index']
                step.updated_at = datetime.utcnow()
        
        db.session.commit()
    
    def get_next_step(self):
        """Retorna a próxima etapa ativa do funil"""
        return FunnelStep.query.filter(
            FunnelStep.funnel_id == self.funnel_id,
            FunnelStep.order_index > self.order_index,
            FunnelStep.is_active == True
        ).order_by(FunnelStep.order_index).first()
    
    def get_previous_step(self):
        """Retorna a etapa anterior ativa do funil"""
        return FunnelStep.query.filter(
            FunnelStep.funnel_id == self.funnel_id,
            FunnelStep.order_index < self.order_index,
            FunnelStep.is_active == True
        ).order_by(FunnelStep.order_index.desc()).first()
    
    def __repr__(self):
        return f'<FunnelStep {self.name} - {self.step_type}>'

