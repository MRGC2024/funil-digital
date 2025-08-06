from datetime import datetime
from src.models import db

class VisitorEvent(db.Model):
    """Modelo para eventos de visitantes"""
    
    __tablename__ = 'visitor_events'
    
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitors.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # 'page_view', 'form_submit', 'payment_init', 'payment_complete'
    step_id = db.Column(db.Integer, db.ForeignKey('funnel_steps.id'))
    event_data = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    step = db.relationship('FunnelStep')
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'visitor_id': self.visitor_id,
            'event_type': self.event_type,
            'step_id': self.step_id,
            'step_name': self.step.name if self.step else None,
            'event_data': self.event_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @staticmethod
    def get_events_by_type(event_type, funnel_id=None, start_date=None, end_date=None):
        """Retorna eventos por tipo com filtros opcionais"""
        query = VisitorEvent.query.filter_by(event_type=event_type)
        
        if funnel_id:
            query = query.join(VisitorEvent.step).filter(
                db.text('funnel_steps.funnel_id = :funnel_id')
            ).params(funnel_id=funnel_id)
        
        if start_date:
            query = query.filter(VisitorEvent.created_at >= start_date)
        
        if end_date:
            query = query.filter(VisitorEvent.created_at <= end_date)
        
        return query.all()
    
    @staticmethod
    def get_conversion_funnel(funnel_id, start_date=None, end_date=None):
        """Retorna dados do funil de conversão"""
        from src.models.funnel_step import FunnelStep
        
        # Busca todas as etapas do funil
        steps = FunnelStep.query.filter_by(
            funnel_id=funnel_id, 
            is_active=True
        ).order_by(FunnelStep.order_index).all()
        
        conversion_data = []
        
        for step in steps:
            # Conta page_views para cada etapa
            query = VisitorEvent.query.filter_by(
                event_type='page_view',
                step_id=step.id
            )
            
            if start_date:
                query = query.filter(VisitorEvent.created_at >= start_date)
            
            if end_date:
                query = query.filter(VisitorEvent.created_at <= end_date)
            
            page_views = query.count()
            
            # Conta conversões (form_submit, payment_complete, etc.)
            conversion_query = VisitorEvent.query.filter(
                VisitorEvent.step_id == step.id,
                VisitorEvent.event_type.in_(['form_submit', 'payment_complete'])
            )
            
            if start_date:
                conversion_query = conversion_query.filter(VisitorEvent.created_at >= start_date)
            
            if end_date:
                conversion_query = conversion_query.filter(VisitorEvent.created_at <= end_date)
            
            conversions = conversion_query.count()
            
            conversion_rate = (conversions / page_views * 100) if page_views > 0 else 0
            
            conversion_data.append({
                'step_id': step.id,
                'step_name': step.name,
                'step_type': step.step_type,
                'order_index': step.order_index,
                'page_views': page_views,
                'conversions': conversions,
                'conversion_rate': round(conversion_rate, 2)
            })
        
        return conversion_data
    
    @staticmethod
    def get_hourly_stats(funnel_id=None, date=None):
        """Retorna estatísticas por hora"""
        if not date:
            date = datetime.utcnow().date()
        
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())
        
        query = VisitorEvent.query.filter(
            VisitorEvent.created_at >= start_datetime,
            VisitorEvent.created_at <= end_datetime
        )
        
        if funnel_id:
            query = query.join(VisitorEvent.step).filter(
                db.text('funnel_steps.funnel_id = :funnel_id')
            ).params(funnel_id=funnel_id)
        
        events = query.all()
        
        # Agrupa por hora
        hourly_stats = {}
        for hour in range(24):
            hourly_stats[hour] = {
                'hour': hour,
                'page_views': 0,
                'form_submits': 0,
                'payments': 0,
                'total_events': 0
            }
        
        for event in events:
            hour = event.created_at.hour
            hourly_stats[hour]['total_events'] += 1
            
            if event.event_type == 'page_view':
                hourly_stats[hour]['page_views'] += 1
            elif event.event_type == 'form_submit':
                hourly_stats[hour]['form_submits'] += 1
            elif event.event_type in ['payment_init', 'payment_complete']:
                hourly_stats[hour]['payments'] += 1
        
        return list(hourly_stats.values())
    
    def __repr__(self):
        return f'<VisitorEvent {self.event_type} - Visitor {self.visitor_id}>'

