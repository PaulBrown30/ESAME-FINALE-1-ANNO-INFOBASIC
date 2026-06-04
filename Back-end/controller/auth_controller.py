from flask import Blueprint, jsonify, request, g
from exception.app_exception import AppException
from service import auth_service
from functools import wraps

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/login",)
def login(login_data):

    try:
        token, account = auth_service.login(login_data)
        return jsonify({"token": token, "account": account.to_dict()})

    except AppException as e:
        return jsonify(e.to_dict()),e.status
    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            parti = request.headers["Authorization"].split(" ")
            if len(parti) == 2 and parti[0] == "Bearer":
                token = parti[1]

        if token is None:
            return jsonify({"error": "Token mancante!"}), 401
        
        try:
            payload = auth_service.verifica_token(token)

            g.id = payload["id"]
            g.email = payload["email"]
            g.account_type = payload["account_type"]

        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def role_required(*ammitted_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.user_ruolo not in ammitted_roles:
                return jsonify({"error": "Accesso negato! Ruolo non autorizzato."}), 403

            return f(*args, **kwargs)

        return decorated

    return decorator