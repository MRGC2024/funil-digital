from datetime import datetime, timedelta
from src.models import db

class Visitor(db.Model):
    """Modelo para rastrear visitantes do funil"""
    
    __tablename__ = 'visitors'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))  # Suporta IPv6
    user_agent = db.Column(db.Text)
    funnel_id = db.Column(db.Integer, db.ForeignKey('funnels.id'))
    current_step_id = db.Column(db.Integer, db.ForeignKey('funnel_steps.id'))
    utm_source = db.Column(db.String(255))
    utm_medium = db.Column(db.String(255))
    utm_campaign = db.Column(db.String(255))
    utm_term = db.Column(db.String(255))
    utm_content = db.Column(db.String(255))
    first_visit = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_online = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    current_step = db.relationship('FunnelStep', foreign_keys=[current_step_id])
    events = db.relationship('VisitorEvent', backref='visitor', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='visitor', lazy='dynamic')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'funnel_id': self.funnel_id,
            'current_step_id': self.current_step_id,
            'current_step_name': self.current_step.name if self.current_step else None,
            'utm_source': self.utm_source,
            'utm_medium': self.utm_medium,
            'utm_campaign': self.utm_campaign,
            'utm_term': self.utm_term,
            'utm_content': self.utm_content,
            'first_visit': self.first_visit.isoformat() if self.first_visit else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'is_online': self.is_online,
            'time_on_site': self.get_time_on_site(),
            'events_count': self.events.count()
        }
    
    def to_dict_with_events(self):
        """Converte o modelo para dicionário incluindo eventos"""
        data = self.to_dict()
        data['events'] = [event.to_dict() for event in self.events.order_by('created_at').all()]
        return data
    
    def update_activity(self, step_id=None):
        """Atualiza a última atividade do visitante"""
        self.last_activity = datetime.utcnow()
        self.is_online = True
        
        if step_id and step_id != self.current_step_id:
            self.current_step_id = step_id
    
    def mark_offline(self):
        """Marca o visitante como offline"""
        self.is_online = False
    
    def get_time_on_site(self):
        """Retorna o tempo total no site em segundos"""
        if self.first_visit and self.last_activity:
            delta = self.last_activity - self.first_visit
            return int(delta.total_seconds())
        return 0
    
    def get_time_on_site_formatted(self):
        """Retorna o tempo no site formatado"""
        seconds = self.get_time_on_site()
        
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}m {seconds % 60}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
    
    def add_event(self, event_type, step_id=None, event_data=None):
        """Adiciona um evento para o visitante"""
        from src.models.visitor_event import VisitorEvent
        
        event = VisitorEvent(
            visitor_id=self.id,
            event_type=event_type,
            step_id=step_id,
            event_data=event_data or {}
        )
        
        db.session.add(event)
        self.update_activity(step_id)
        
        return event
    
    @staticmethod
    def get_online_visitors(funnel_id=None):
        """Retorna visitantes online"""
        # Considera online visitantes com atividade nos últimos 5 minutos
        cutoff_time = datetime.utcnow() - timedelta(minutes=5)
        
        query = Visitor.query.filter(
            Visitor.last_activity >= cutoff_time,
            Visitor.is_online == True
        )
        
        if funnel_id:
            query = query.filter(Visitor.funnel_id == funnel_id)
        
        return query.all()
    
    @staticmethod
    def cleanup_old_visitors(days=30):
        """Remove visitantes antigos (mais de X dias)"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_visitors = Visitor.query.filter(
            Visitor.last_activity < cutoff_date
        ).all()
        
        for visitor in old_visitors:
            db.session.delete(visitor)
        
        db.session.commit()
        return len(old_visitors)
    
    @staticmethod
    def mark_inactive_offline():
        """Marca visitantes inativos como offline"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=5)
        
        inactive_visitors = Visitor.query.filter(
            Visitor.last_activity < cutoff_time,
            Visitor.is_online == True
        ).all()
        
        for visitor in inactive_visitors:
            visitor.mark_offline()
        
        db.session.commit()
        return len(inactive_visitors)
    
    def __repr__(self):
        return f'<Visitor {self.session_id} - {self.ip_address}>'

