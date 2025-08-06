from datetime import datetime
from decimal import Decimal
from src.models import db

class CheckoutConfig(db.Model):
    """Modelo para configurações de checkout"""
    
    __tablename__ = 'checkout_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    funnel_id = db.Column(db.Integer, db.ForeignKey('funnels.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('funnel_steps.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_price = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='BRL')
    payment_methods = db.Column(db.JSON, default=['pix'])
    fields_config = db.Column(db.JSON, default={})
    design_config = db.Column(db.JSON, default={})
    upsell_config = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'funnel_id': self.funnel_id,
            'step_id': self.step_id,
            'product_name': self.product_name,
            'product_price': float(self.product_price) if self.product_price else 0,
            'currency': self.currency,
            'payment_methods': self.payment_methods,
            'fields_config': self.fields_config,
            'design_config': self.design_config,
            'upsell_config': self.upsell_config,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def clone(self, new_funnel_id, new_step_id=None):
        """Clona a configuração de checkout para um novo funil"""
        new_checkout = CheckoutConfig(
            funnel_id=new_funnel_id,
            step_id=new_step_id or self.step_id,
            product_name=self.product_name,
            product_price=self.product_price,
            currency=self.currency,
            payment_methods=self.payment_methods.copy() if self.payment_methods else ['pix'],
            fields_config=self.fields_config.copy() if self.fields_config else {},
            design_config=self.design_config.copy() if self.design_config else {},
            upsell_config=self.upsell_config.copy() if self.upsell_config else {}
        )
        return new_checkout
    
    def get_price_in_cents(self):
        """Retorna o preço em centavos para APIs de pagamento"""
        return int(self.product_price * 100) if self.product_price else 0
    
    def update_design(self, design_data):
        """Atualiza a configuração de design"""
        if not self.design_config:
            self.design_config = {}
        
        self.design_config.update(design_data)
        self.updated_at = datetime.utcnow()
    
    def update_fields(self, fields_data):
        """Atualiza a configuração de campos"""
        if not self.fields_config:
            self.fields_config = {}
        
        self.fields_config.update(fields_data)
        self.updated_at = datetime.utcnow()
    
    def update_upsell(self, upsell_data):
        """Atualiza a configuração de upsell"""
        if not self.upsell_config:
            self.upsell_config = {}
        
        self.upsell_config.update(upsell_data)
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<CheckoutConfig {self.product_name} - R$ {self.product_price}>'

