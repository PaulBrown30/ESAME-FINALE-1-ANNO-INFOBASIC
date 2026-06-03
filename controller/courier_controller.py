from flask import Blueprint,jsonify,request
from service import courier_service
from exception.app_exception import AppException

courier_bp = Blueprint("courier",__name__,url_prefix="/api")

@courier_bp.route("/couriers/<int:courier_id>")
def get_by_id(courier_id):   
    try:
        courier = courier_service.get_by_id(courier_id)
        return jsonify(courier.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@courier_bp.route("/couriers")
def get_all():   
    try:
        couriers = courier_service.get_all()
        return jsonify([c.to_dict() for c in couriers]),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@courier_bp.route("/couriers/available")
def get_available_couriers():
    try:
        couriers = courier_service.get_available_couriers()
        return jsonify([c.to_dict() for c in couriers]),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status    

@courier_bp.route("/couriers/create", methods = ["POST"])
def create():
    try:
        dati_courier = request.get_json()
        admin = courier_service.create(dati_courier)
        return jsonify(admin.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status
   
@courier_bp.route("/couriers/<int:courier_id>", methods = ["PATCH"])
def update(courier_id):  
    try:
        dati_courier = request.get_json()
        courier = courier_service.update(courier_id,dati_courier)
        return jsonify(courier.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status

@courier_bp.route("/couriers/<int:courier_id>", methods= ["DELETE"])
def delete_by_id(courier_id):
    try:
        courier_service.delete_by_id(courier_id)
        return jsonify({"message":"Il corriere è stato eliminato correttamente","status":200})

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
            