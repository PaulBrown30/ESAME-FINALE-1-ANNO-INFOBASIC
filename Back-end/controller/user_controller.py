from flask import Blueprint,jsonify,request
from service import user_service
from exception.app_exception import AppException
from controller.auth_controller import token_required

user_bp = Blueprint("user",__name__,url_prefix="/api")

@user_bp.route("/users/<int:user_id>")
@token_required
def get_by_id(user_id):
    
    try:
        admin = user_service.get_by_id(user_id)
        return jsonify(admin.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@user_bp.route("/users/create",methods = ["POST"])
def create():
    try:
        dati_user = request.get_json()
        user = user_service.create(dati_user)
        return jsonify(user.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@user_bp.route("/users/<int:user_id>/add_package", methods = ["POST"])
def add_package(user_id):
    
    try:
        package_id = request.get_json()["package_id"]
        package_added = user_service.add_package(user_id,package_id)
        return jsonify(package_added.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status  