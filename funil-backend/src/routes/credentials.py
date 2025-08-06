from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.routes import credentials_bp
from src.models import db
from src.models.credential import Credential

@credentials_bp.route("/", methods=["GET"])
@jwt_required()
def get_credentials():
    credentials = Credential.query.all()
    return jsonify([cred.to_dict() for cred in credentials]), 200

@credentials_bp.route("/", methods=["POST"])
@jwt_required()
def create_credential():
    data = request.get_json()
    name = data.get("name")
    service = data.get("service")
    api_key = data.get("api_key")
    api_secret = data.get("api_secret")
    api_url = data.get("api_url")
    current_user_id = get_jwt_identity()

    if not all([name, service, api_key]):
        return jsonify({"msg": "Missing required fields"}), 400

    new_credential = Credential(
        name=name,
        service=service,
        api_key=api_key,
        api_secret=api_secret,
        api_url=api_url,
        created_by=current_user_id
    )
    db.session.add(new_credential)
    db.session.commit()
    return jsonify(new_credential.to_dict()), 201

@credentials_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_credential(id):
    credential = Credential.query.get_or_404(id)
    data = request.get_json()

    credential.name = data.get("name", credential.name)
    credential.service = data.get("service", credential.service)
    credential.api_key = data.get("api_key", credential.api_key)
    credential.api_secret = data.get("api_secret", credential.api_secret)
    credential.api_url = data.get("api_url", credential.api_url)
    credential.is_active = data.get("is_active", credential.is_active)

    db.session.commit()
    return jsonify(credential.to_dict()), 200

@credentials_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_credential(id):
    credential = Credential.query.get_or_404(id)
    db.session.delete(credential)
    db.session.commit()
    return jsonify({"msg": "Credential deleted"}), 204

