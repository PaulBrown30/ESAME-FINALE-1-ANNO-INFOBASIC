from flask import Blueprint,jsonify,request
from service import status_service
from exception.app_exception import AppException

status_bp = Blueprint("status",__name__,url_prefix="/api")

@status_bp.route("/statuses/<int:status_id>")
def get_by_id(status_id):   
    try:
        status = status_service.get_by_id(status_id)
        return jsonify(status.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    
@status_bp.route("/statuses")
def get_all():   
    try:
        statuses = status_service.get_all()
        return jsonify([s.to_dict() for s in statuses]),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status    

@status_bp.route("/statuses/create")
def create():
    try:
        dati_status = request.get_json()
        status = status_service.create(dati_status)
        return jsonify(status.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status