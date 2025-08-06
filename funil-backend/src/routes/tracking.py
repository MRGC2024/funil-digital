from flask import request, jsonify
from flask_jwt_extended import jwt_required
from src.routes import tracking_bp
from src.models import db
from src.models.tracking_pixel import TrackingPixel
from src.models.funnel import Funnel
from src.models.funnel_step import FunnelStep

@tracking_bp.route("/pixels", methods=["GET"])
@jwt_required()
def get_pixels():
    funnel_id = request.args.get("funnel_id", type=int)
    step_id = request.args.get("step_id", type=int)
    
    if funnel_id:
        pixels = TrackingPixel.get_funnel_pixels(funnel_id, step_id)
    else:
        pixels = TrackingPixel.query.all()
        
    return jsonify([pixel.to_dict() for pixel in pixels]), 200

@tracking_bp.route("/pixels", methods=["POST"])
@jwt_required()
def create_pixel():
    data = request.get_json()
    funnel_id = data.get("funnel_id")
    step_id = data.get("step_id")
    pixel_type = data.get("pixel_type")
    pixel_id = data.get("pixel_id")
    event_name = data.get("event_name")

    if not all([funnel_id, pixel_type, pixel_id]):
        return jsonify({"msg": "Missing required fields"}), 400

    funnel = Funnel.query.get_or_404(funnel_id)
    if step_id:
        FunnelStep.query.filter_by(funnel_id=funnel_id, id=step_id).first_or_404()

    new_pixel = TrackingPixel(
        funnel_id=funnel_id,
        step_id=step_id,
        pixel_type=pixel_type,
        pixel_id=pixel_id,
        event_name=event_name
    )
    db.session.add(new_pixel)
    db.session.commit()
    return jsonify(new_pixel.to_dict()), 201

@tracking_bp.route("/pixels/<int:id>", methods=["PUT"])
@jwt_required()
def update_pixel(id):
    pixel = TrackingPixel.query.get_or_404(id)
    data = request.get_json()

    pixel.funnel_id = data.get("funnel_id", pixel.funnel_id)
    pixel.step_id = data.get("step_id", pixel.step_id)
    pixel.pixel_type = data.get("pixel_type", pixel.pixel_type)
    pixel.pixel_id = data.get("pixel_id", pixel.pixel_id)
    pixel.event_name = data.get("event_name", pixel.event_name)
    pixel.is_active = data.get("is_active", pixel.is_active)

    db.session.commit()
    return jsonify(pixel.to_dict()), 200

@tracking_bp.route("/pixels/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_pixel(id):
    pixel = TrackingPixel.query.get_or_404(id)
    db.session.delete(pixel)
    db.session.commit()
    return jsonify({"msg": "Tracking pixel deleted"}), 204

@tracking_bp.route("/pixels/<int:funnel_id>/<int:step_id>/render", methods=["GET"])
def render_pixels(funnel_id, step_id):
    pixels = TrackingPixel.get_funnel_pixels(funnel_id, step_id)
    scripts = "\n".join([pixel.generate_script() for pixel in pixels])
    return scripts, 200, {"Content-Type": "text/html"}

