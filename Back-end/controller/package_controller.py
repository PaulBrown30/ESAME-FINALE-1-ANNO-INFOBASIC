from flask import Blueprint,jsonify,request
from service import package_service
from exception.app_exception import AppException

package_bp = Blueprint("package",__name__,url_prefix="/api")

@package_bp.route("/packages/<package_id>")
def get_by_id(package_id):   
    try:
        package = package_service.get_by_id(package_id)
        return jsonify(package.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@package_bp.route("/packages")
def get_all():   
    try:
        packages = package_service.get_all()
        return jsonify([p.to_dict() for p in packages]),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status    

@package_bp.route("/packages/create", methods = ["POST"])
def create():
    try:
        dati_package = request.get_json()
        package = package_service.create(dati_package)
        return jsonify(package.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status
   
@package_bp.route("/packages/<package_id>", methods = ["DELETE"])
def delete_by_id(package_id):
    try:
        package_service.delete_by_id(package_id)
        return jsonify({"message":"Il pacco è stato eliminato correttamente","status":200})

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@package_bp.route("/packages/<package_id>/add_status", methods = ["POST"])
def add_status(package_id):
    
    try:
        status_id = request.get_json()
        package_service.add_status(package_id,status_id)
        return jsonify({"message":f"Lo stato {status_id["status_id"]} è stato aggiunto correttamente","status":200})
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@package_bp.route("/packages/<package_id>/set_inactive", methods = ["PATCH"])
def set_inactive(package_id):
    
    try:
        package_service.set_inactive(package_id)
        return jsonify({"message":f"Il pacco {package_id} è stato reso inattivo","status":200})       

    except AppException as e:
        return jsonify(e.to_dict()),e.status