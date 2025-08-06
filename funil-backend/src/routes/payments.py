from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.routes import payments_bp
from src.models import db
from src.models.payment import Payment
from src.models.visitor import Visitor
from src.models.funnel import Funnel
from src.models.funnel_step import FunnelStep
from src.models.checkout_config import CheckoutConfig
from src.models.credential import Credential
import requests

@payments_bp.route("/create", methods=["POST"])
# @jwt_required() # Pode ser acessado por funil, sem JWT
def create_payment():
    data = request.get_json()
    visitor_id = data.get("visitor_id")
    funnel_id = data.get("funnel_id")
    step_id = data.get("step_id")
    customer_data = data.get("customer_data", {})

    if not all([visitor_id, funnel_id, step_id, customer_data]):
        return jsonify({"msg": "Missing required fields"}), 400

    visitor = Visitor.query.get(visitor_id)
    funnel = Funnel.query.get(funnel_id)
    step = FunnelStep.query.get(step_id)
    checkout_config = CheckoutConfig.query.filter_by(funnel_id=funnel_id, step_id=step_id).first()

    if not all([visitor, funnel, step, checkout_config]):
        return jsonify({"msg": "Invalid visitor, funnel, step or checkout configuration"}), 404

    skalepay_credential = Credential.get_active_by_service("skalepay")
    if not skalepay_credential:
        return jsonify({"msg": "SkalePay credentials not configured"}), 500

    amount_in_cents = checkout_config.get_price_in_cents()

    # Simula chamada à API SkalePay
    try:
        # Exemplo de payload para SkalePay (adaptar conforme a documentação real da API)
        skalepay_payload = {
            "amount": amount_in_cents,
            "currency": "BRL",
            "customer": {
                "name": customer_data.get("name"),
                "email": customer_data.get("email"),
                "document": customer_data.get("cpf"),
                "phone": customer_data.get("phone"),
            },
            "description": f"Pagamento para {checkout_config.product_name}",
            "callback_url": f"{skalepay_credential.api_url}/webhook", # Exemplo de webhook
            "reference_id": f"funnel_{funnel_id}_step_{step_id}_visitor_{visitor_id}"
        }
        
        headers = {
            "Authorization": f"Basic {skalepay_credential.api_key}", # Assumindo API Key é o secret
            "Content-Type": "application/json"
        }
        
        # response = requests.post(f"{skalepay_credential.api_url}/payments", json=skalepay_payload, headers=headers)
        # response.raise_for_status() # Levanta exceção para erros HTTP
        # skalepay_response = response.json()

        # Simulação de resposta da SkalePay
        skalepay_response = {
            "id": "pix_simulado_12345",
            "status": "pending",
            "qr_code_image": "https://via.placeholder.com/150?text=QR+Code",
            "qr_code_text": "00020126580014BR.GOV.BCB.PIX0136a6239612-42b7-45a7-937b-94c7c7d2d3e4520400005303986540510.005802BR6007BRASIL62070503***6304E821",
            "amount": amount_in_cents / 100
        }

        new_payment = Payment(
            visitor_id=visitor_id,
            funnel_id=funnel_id,
            step_id=step_id,
            external_id=skalepay_response.get("id"),
            amount=skalepay_response.get("amount"),
            currency=skalepay_payload.get("currency"),
            status=skalepay_response.get("status"),
            payment_method="pix",
            customer_data=customer_data,
            gateway_response=skalepay_response
        )
        db.session.add(new_payment)
        db.session.commit()
        
        visitor.add_event("payment_init", step_id, {"payment_id": new_payment.id, "amount": new_payment.amount})
        db.session.commit()

        return jsonify(new_payment.to_dict()), 201

    except requests.exceptions.RequestException as e:
        return jsonify({"msg": f"Error communicating with SkalePay API: {str(e)}"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"An unexpected error occurred: {str(e)}"}), 500

@payments_bp.route("/<int:payment_id>/status", methods=["GET"])
@jwt_required()
def get_payment_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.to_dict()), 200

@payments_bp.route("/webhook", methods=["POST"])
def payment_webhook():
    data = request.get_json()
    # Exemplo de tratamento de webhook da SkalePay
    payment_external_id = data.get("id")
    new_status = data.get("status")

    payment = Payment.query.filter_by(external_id=payment_external_id).first()

    if not payment:
        return jsonify({"msg": "Payment not found"}), 404

    if payment.status != new_status:
        payment.update_status(new_status, data) # Atualiza status e adiciona dados do webhook
        db.session.commit()
        
        # Opcional: Notificar o dashboard via WebSocket
        # from src.main import socketio
        # socketio.emit("payment_status_change", payment.to_dict())

    return jsonify({"msg": "Webhook received and processed"}), 200

@payments_bp.route("/analytics", methods=["GET"])
@jwt_required()
def get_payment_analytics():
    funnel_id = request.args.get("funnel_id", type=int)
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")

    from datetime import datetime
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

    revenue_stats = Payment.get_revenue_stats(funnel_id, start_date, end_date)
    daily_revenue = Payment.get_daily_revenue(funnel_id, days=7) # Últimos 7 dias
    payment_methods_stats = Payment.get_payment_methods_stats(funnel_id, start_date, end_date)

    return jsonify({
        "revenue_stats": revenue_stats,
        "daily_revenue": daily_revenue,
        "payment_methods_stats": payment_methods_stats
    }), 200

