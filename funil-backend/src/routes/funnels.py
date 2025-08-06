from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.routes import funnels_bp
from src.models import db
from src.models.funnel import Funnel
from src.models.funnel_step import FunnelStep

@funnels_bp.route("/", methods=["GET"])
@jwt_required()
def get_funnels():
    funnels = Funnel.query.all()
    return jsonify([funnel.to_dict() for funnel in funnels]), 200

@funnels_bp.route("/", methods=["POST"])
@jwt_required()
def create_funnel():
    data = request.get_json()
    name = data.get("name")
    slug = data.get("slug")
    description = data.get("description")
    niche = data.get("niche")
    current_user_id = get_jwt_identity()

    if not all([name, slug]):
        return jsonify({"msg": "Missing required fields: name or slug"}), 400

    if Funnel.query.filter_by(slug=slug).first():
        return jsonify({"msg": "Funnel with that slug already exists"}), 409

    new_funnel = Funnel(
        name=name,
        slug=slug,
        description=description,
        niche=niche,
        created_by=current_user_id
    )
    db.session.add(new_funnel)
    db.session.commit()
    return jsonify(new_funnel.to_dict()), 201

@funnels_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_funnel(id):
    funnel = Funnel.query.get_or_404(id)
    return jsonify(funnel.to_dict_with_steps()), 200

@funnels_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_funnel(id):
    funnel = Funnel.query.get_or_404(id)
    data = request.get_json()

    funnel.name = data.get("name", funnel.name)
    funnel.slug = data.get("slug", funnel.slug)
    funnel.description = data.get("description", funnel.description)
    funnel.niche = data.get("niche", funnel.niche)
    funnel.is_active = data.get("is_active", funnel.is_active)
    funnel.settings = data.get("settings", funnel.settings)

    db.session.commit()
    return jsonify(funnel.to_dict()), 200

@funnels_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_funnel(id):
    funnel = Funnel.query.get_or_404(id)
    db.session.delete(funnel)
    db.session.commit()
    return jsonify({"msg": "Funnel deleted"}), 204

@funnels_bp.route("/<int:id>/clone", methods=["POST"])
@jwt_required()
def clone_funnel(id):
    funnel = Funnel.query.get_or_404(id)
    data = request.get_json()
    new_name = data.get("new_name")
    new_slug = data.get("new_slug")
    current_user_id = get_jwt_identity()

    if not all([new_name, new_slug]):
        return jsonify({"msg": "Missing new_name or new_slug"}), 400

    if Funnel.query.filter_by(slug=new_slug).first():
        return jsonify({"msg": "Funnel with that new slug already exists"}), 409

    try:
        cloned_funnel = funnel.clone(new_name, new_slug, current_user_id)
        db.session.add(cloned_funnel)
        db.session.commit()
        return jsonify(cloned_funnel.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error cloning funnel: {str(e)}"}), 500

# Rotas para Etapas do Funil
@funnels_bp.route("/<int:funnel_id>/steps", methods=["GET"])
@jwt_required()
def get_funnel_steps(funnel_id):
    funnel = Funnel.query.get_or_404(funnel_id)
    steps = funnel.steps.order_by(FunnelStep.order_index).all()
    return jsonify([step.to_dict() for step in steps]), 200

@funnels_bp.route("/<int:funnel_id>/steps", methods=["POST"])
@jwt_required()
def create_funnel_step(funnel_id):
    funnel = Funnel.query.get_or_404(funnel_id)
    data = request.get_json()
    name = data.get("name")
    slug = data.get("slug")
    step_type = data.get("step_type")
    order_index = data.get("order_index")

    if not all([name, slug, step_type, order_index is not None]):
        return jsonify({"msg": "Missing required fields"}), 400

    if FunnelStep.query.filter_by(funnel_id=funnel_id, slug=slug).first():
        return jsonify({"msg": "Step with that slug already exists in this funnel"}), 409

    new_step = FunnelStep(
        funnel_id=funnel_id,
        name=name,
        slug=slug,
        step_type=step_type,
        order_index=order_index,
        settings=data.get("settings", {}),
        content=data.get("content", {})
    )
    db.session.add(new_step)
    db.session.commit()
    return jsonify(new_step.to_dict()), 201

@funnels_bp.route("/<int:funnel_id>/steps/<int:step_id>", methods=["PUT"])
@jwt_required()
def update_funnel_step(funnel_id, step_id):
    step = FunnelStep.query.filter_by(funnel_id=funnel_id, id=step_id).first_or_404()
    data = request.get_json()

    step.name = data.get("name", step.name)
    step.slug = data.get("slug", step.slug)
    step.step_type = data.get("step_type", step.step_type)
    step.order_index = data.get("order_index", step.order_index)
    step.is_active = data.get("is_active", step.is_active)
    step.settings = data.get("settings", step.settings)
    step.content = data.get("content", step.content)

    db.session.commit()
    return jsonify(step.to_dict()), 200

@funnels_bp.route("/<int:funnel_id>/steps/<int:step_id>", methods=["DELETE"])
@jwt_required()
def delete_funnel_step(funnel_id, step_id):
    step = FunnelStep.query.filter_by(funnel_id=funnel_id, id=step_id).first_or_404()
    db.session.delete(step)
    db.session.commit()
    return jsonify({"msg": "Funnel step deleted"}), 204

@funnels_bp.route("/<int:funnel_id>/steps/reorder", methods=["PUT"])
@jwt_required()
def reorder_funnel_steps(funnel_id):
    data = request.get_json()
    step_orders = data.get("step_orders")

    if not isinstance(step_orders, list):
        return jsonify({"msg": "step_orders must be a list"}), 400

    try:
        FunnelStep.reorder_steps(funnel_id, step_orders)
        return jsonify({"msg": "Steps reordered successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Error reordering steps: {str(e)}"}), 500

