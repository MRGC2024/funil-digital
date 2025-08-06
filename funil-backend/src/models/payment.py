from datetime import datetime
from decimal import Decimal
from src.models import db

class Payment(db.Model):
    """Modelo para pagamentos"""
    
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'))
    funnel_id = db.Column(db.Integer, db.ForeignKey('funnels.id'))
    step_id = db.Column(db.Integer, db.ForeignKey('funnel_steps.id'))
    external_id = db.Column(db.String(255))  # ID do gateway de pagamento
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='BRL')
    status = db.Column(db.String(50), default='pending')  # 'pending', 'paid', 'failed', 'cancelled'
    payment_method = db.Column(db.String(50), default='pix')
    customer_data = db.Column(db.JSON, default={})
    gateway_response = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'visitor_id': self.visitor_id,
            'funnel_id': self.funnel_id,
            'step_id': self.step_id,
            'external_id': self.external_id,
            'amount': float(self.amount) if self.amount else 0,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'customer_data': self.customer_data,
            'gateway_response': self.gateway_response,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_summary(self):
        """Converte o modelo para dicionário resumido"""
        return {
            'id': self.id,
            'external_id': self.external_id,
            'amount': float(self.amount) if self.amount else 0,
            'currency': self.currency,
            'status': self.status,
            'payment_method': self.payment_method,
            'customer_name': self.customer_data.get('name', 'N/A') if self.customer_data else 'N/A',
            'customer_email': self.customer_data.get('email', 'N/A') if self.customer_data else 'N/A',
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def update_status(self, new_status, gateway_response=None):
        """Atualiza o status do pagamento"""
        self.status = new_status
        self.updated_at = datetime.utcnow()
        
        if gateway_response:
            if not self.gateway_response:
                self.gateway_response = {}
            self.gateway_response.update(gateway_response)
        
        # Adiciona evento de mudança de status
        if self.visitor_id:
            from src.models.visitor import Visitor
            visitor = Visitor.query.get(self.visitor_id)
            if visitor:
                event_data = {
                    'payment_id': self.id,
                    'old_status': self.status,
                    'new_status': new_status,
                    'amount': float(self.amount)
                }
                visitor.add_event('payment_status_change', self.step_id, event_data)
    
    def get_amount_in_cents(self):
        """Retorna o valor em centavos"""
        return int(self.amount * 100) if self.amount else 0
    
    def is_paid(self):
        """Verifica se o pagamento foi aprovado"""
        return self.status == 'paid'
    
    def is_pending(self):
        """Verifica se o pagamento está pendente"""
        return self.status == 'pending'
    
    def is_failed(self):
        """Verifica se o pagamento falhou"""
        return self.status in ['failed', 'cancelled']
    
    @staticmethod
    def get_revenue_stats(funnel_id=None, start_date=None, end_date=None):
        """Retorna estatísticas de receita"""
        query = Payment.query.filter_by(status='paid')
        
        if funnel_id:
            query = query.filter_by(funnel_id=funnel_id)
        
        if start_date:
            query = query.filter(Payment.created_at >= start_date)
        
        if end_date:
            query = query.filter(Payment.created_at <= end_date)
        
        payments = query.all()
        
        total_revenue = sum(float(p.amount) for p in payments)
        total_transactions = len(payments)
        average_ticket = total_revenue / total_transactions if total_transactions > 0 else 0
        
        return {
            'total_revenue': round(total_revenue, 2),
            'total_transactions': total_transactions,
            'average_ticket': round(average_ticket, 2),
            'currency': 'BRL'
        }
    
    @staticmethod
    def get_daily_revenue(funnel_id=None, days=30):
        """Retorna receita diária dos últimos X dias"""
        from datetime import timedelta
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        query = Payment.query.filter(
            Payment.status == 'paid',
            Payment.created_at >= start_date,
            Payment.created_at <= end_date
        )
        
        if funnel_id:
            query = query.filter_by(funnel_id=funnel_id)
        
        payments = query.all()
        
        # Agrupa por dia
        daily_revenue = {}
        current_date = start_date.date()
        
        while current_date <= end_date.date():
            daily_revenue[current_date.isoformat()] = {
                'date': current_date.isoformat(),
                'revenue': 0,
                'transactions': 0
            }
            current_date += timedelta(days=1)
        
        for payment in payments:
            date_key = payment.created_at.date().isoformat()
            if date_key in daily_revenue:
                daily_revenue[date_key]['revenue'] += float(payment.amount)
                daily_revenue[date_key]['transactions'] += 1
        
        return list(daily_revenue.values())
    
    @staticmethod
    def get_payment_methods_stats(funnel_id=None, start_date=None, end_date=None):
        """Retorna estatísticas por método de pagamento"""
        query = Payment.query.filter_by(status='paid')
        
        if funnel_id:
            query = query.filter_by(funnel_id=funnel_id)
        
        if start_date:
            query = query.filter(Payment.created_at >= start_date)
        
        if end_date:
            query = query.filter(Payment.created_at <= end_date)
        
        payments = query.all()
        
        methods_stats = {}
        for payment in payments:
            method = payment.payment_method
            if method not in methods_stats:
                methods_stats[method] = {
                    'method': method,
                    'count': 0,
                    'revenue': 0
                }
            
            methods_stats[method]['count'] += 1
            methods_stats[method]['revenue'] += float(payment.amount)
        
        return list(methods_stats.values())
    
    def __repr__(self):
        return f'<Payment {self.external_id} - R$ {self.amount} - {self.status}>'

