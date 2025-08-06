from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.routes import checkout_bp
from src.models import db
from src.models.checkout_config import CheckoutConfig
from src.models.funnel import Funnel
from src.models.funnel_step import FunnelStep

@checkout_bp.route("/<int:funnel_id>/<int:step_id>", methods=["GET"])
@jwt_required()
def get_checkout_config(funnel_id, step_id):
    checkout_config = CheckoutConfig.query.filter_by(funnel_id=funnel_id, step_id=step_id).first_or_404()
    return jsonify(checkout_config.to_dict()), 200

@checkout_bp.route("/<int:funnel_id>/<int:step_id>", methods=["POST"])
@jwt_required()
def create_checkout_config(funnel_id, step_id):
    Funnel.query.get_or_404(funnel_id)
    FunnelStep.query.filter_by(funnel_id=funnel_id, id=step_id).first_or_404()

    data = request.get_json()
    product_name = data.get("product_name")
    product_price = data.get("product_price")

    if not all([product_name, product_price]):
        return jsonify({"msg": "Missing product_name or product_price"}), 400

    existing_config = CheckoutConfig.query.filter_by(funnel_id=funnel_id, step_id=step_id).first()
    if existing_config:
        return jsonify({"msg": "Checkout configuration already exists for this step"}), 409

    new_config = CheckoutConfig(
        funnel_id=funnel_id,
        step_id=step_id,
        product_name=product_name,
        product_price=product_price,
        currency=data.get("currency", "BRL"),
        payment_methods=data.get("payment_methods", ["pix"]),
        fields_config=data.get("fields_config", {}),
        design_config=data.get("design_config", {}),
        upsell_config=data.get("upsell_config", {})
    )
    db.session.add(new_config)
    db.session.commit()
    return jsonify(new_config.to_dict()), 201

@checkout_bp.route("/<int:funnel_id>/<int:step_id>", methods=["PUT"])
@jwt_required()
def update_checkout_config(funnel_id, step_id):
    checkout_config = CheckoutConfig.query.filter_by(funnel_id=funnel_id, step_id=step_id).first_or_404()
    data = request.get_json()

    checkout_config.product_name = data.get("product_name", checkout_config.product_name)
    checkout_config.product_price = data.get("product_price", checkout_config.product_price)
    checkout_config.currency = data.get("currency", checkout_config.currency)
    checkout_config.payment_methods = data.get("payment_methods", checkout_config.payment_methods)
    checkout_config.fields_config = data.get("fields_config", checkout_config.fields_config)
    checkout_config.design_config = data.get("design_config", checkout_config.design_config)
    checkout_config.upsell_config = data.get("upsell_config", checkout_config.upsell_config)

    db.session.commit()
    return jsonify(checkout_config.to_dict()), 200

@checkout_bp.route("/<int:funnel_id>/<int:step_id>", methods=["DELETE"])
@jwt_required()
def delete_checkout_config(funnel_id, step_id):
    checkout_config = CheckoutConfig.query.filter_by(funnel_id=funnel_id, step_id=step_id).first_or_404()
    db.session.delete(checkout_config)
    db.session.commit()
    return jsonify({"msg": "Checkout configuration deleted"}), 204

@checkout_bp.route("/<int:funnel_id>/<int:step_id>/preview", methods=["GET"])
@jwt_required()
def preview_checkout(funnel_id, step_id):
    checkout_config = CheckoutConfig.query.filter_by(funnel_id=funnel_id, step_id=step_id).first_or_404()
    # Aqui você pode renderizar um HTML com base nas configurações ou retornar os dados para o frontend renderizar
    return jsonify({
        "msg": "Checkout preview data",
        "data": checkout_config.to_dict()
    }), 200

