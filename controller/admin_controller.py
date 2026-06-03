from flask import Blueprint,jsonify,request
from service import admin_service
from exception.app_exception import AppException

admin_bp = Blueprint("admin",__name__,url_prefix="/api")

@admin_bp.route("/admin/<int:admin_id>")
def get_by_id(admin_id):
    
    try:
        admin = admin_service.get_by_id(admin_id)
        return jsonify(admin.to_dict()),200
    
    except AppException as e:
        return jsonify(e.to_dict()),e.status
    

@admin_bp.route("/admin/create",methods = ["POST"])
def create():
    try:
        dati_admin = request.get_json()
        admin = admin_service.create(dati_admin)
        return jsonify(admin.to_dict()),200

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    



        
