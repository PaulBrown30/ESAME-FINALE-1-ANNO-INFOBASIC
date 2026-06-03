from flask import Blueprint,jsonify,request
from service import package_service
from exception.app_exception import AppException

package_bp = Blueprint("package",__name__,url_prefix="/api")

@package_bp.route("/package/<int:package_id>")
def get_by_id(package_id):   
    try:
        package = package_service.get_by_id(package_id)
        return jsonify(package.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@package_bp.route("/package")
def get_all():   
    try:
        packages = package_service.get_all()
        return jsonify([p.to_dict() for p in packages]),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status    

@package_bp.route("/package/create")
def create():
    try:
        dati_package = request.get_json()
        package = package_service.create(dati_package)
        return jsonify(package.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status
   
@package_bp.route("/package/<int:package_id>", methods = ["DELETE"])
def delete_by_id(package_id):
    try:
        package_service.delete_by_id(package_id)
        return jsonify({"message":"Il pacco è stato eliminato correttamente","status":200})

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@package_bp.route("/package/<int:package_id>", methods = ["PATCH"])
def add_status(package_id):
    
    try:
        status_id = request.get_json()
        package_service.add_status(package_id,status_id)
        return jsonify({"message":f"Lo stato {status_id} è stato aggiunto correttamente","status":200})
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status  
            