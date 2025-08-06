from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.routes import monitoring_bp
from src.models.visitor import Visitor
from src.models.visitor_event import VisitorEvent
from src.models.funnel import Funnel

@monitoring_bp.route("/visitors", methods=["GET"])
@jwt_required()
def get_online_visitors():
    funnel_id = request.args.get("funnel_id", type=int)
    visitors = Visitor.get_online_visitors(funnel_id=funnel_id)
    return jsonify([visitor.to_dict() for visitor in visitors]), 200

@monitoring_bp.route("/visitors/<int:visitor_id>/events", methods=["GET"])
@jwt_required()
def get_visitor_events(visitor_id):
    visitor = Visitor.query.get_or_404(visitor_id)
    return jsonify([event.to_dict() for event in visitor.events.all()]), 200

@monitoring_bp.route("/analytics/dashboard", methods=["GET"])
@jwt_required()
def get_dashboard_analytics():
    funnel_id = request.args.get("funnel_id", type=int)
    
    # Exemplo de dados para o dashboard
    total_funnels = Funnel.query.count()
    total_visitors = Visitor.query.count()
    online_visitors = Visitor.get_online_visitors(funnel_id=funnel_id)
    
    # Obter estatísticas de conversão do funil
    conversion_data = []
    if funnel_id:
        conversion_data = VisitorEvent.get_conversion_funnel(funnel_id)
    
    # Obter estatísticas de receita (exemplo, precisa de mais dados de pagamento)
    from src.models.payment import Payment
    revenue_stats = Payment.get_revenue_stats(funnel_id=funnel_id)
    
    return jsonify({
        "total_funnels": total_funnels,
        "total_visitors": total_visitors,
        "online_visitors_count": len(online_visitors),
        "online_visitors": [v.to_dict() for v in online_visitors],
        "conversion_data": conversion_data,
        "revenue_stats": revenue_stats
    }), 200

@monitoring_bp.route("/analytics/hourly", methods=["GET"])
@jwt_required()
def get_hourly_analytics():
    funnel_id = request.args.get("funnel_id", type=int)
    date_str = request.args.get("date")
    
    date = None
    if date_str:
        from datetime import datetime
        try:
            date = datetime.strptime(date_str, ")%Y-%m-%d").date()
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    hourly_stats = VisitorEvent.get_hourly_stats(funnel_id=funnel_id, date=date)
    return jsonify(hourly_stats), 200

