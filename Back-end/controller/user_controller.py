from flask import Blueprint,jsonify,request
from service import user_service
from exception.app_exception import AppException

user_bp = Blueprint("user",__name__,url_prefix="/api")

@user_bp.route("/users/<int:user_id>")
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
    
@user_bp.route("/users/<int:user_id>", methods = ["PATCH"])
def add_package(user_id):
    
    try:
        package_id = request.get_json()
        user_service.add_package(user_id,package_id)
        return jsonify({"message":f"Il pacco {package_id["package_id"]} è stato aggiunto correttamente","status":200})
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status  