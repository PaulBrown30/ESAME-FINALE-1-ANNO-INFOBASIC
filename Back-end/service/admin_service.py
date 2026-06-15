from persistence.db_config import get_session
from repository import account_repository, admin_repository
from exception.app_exception import AppException
from model.admin_model import Admin
import re
import bcrypt

def get_by_id(admin_id):
    with get_session() as session:

        admin = admin_repository.get_by_id(session,admin_id)

        if admin is None:
            raise AppException("Nessun admin trovato",404)

        return admin

def create(admin_data):
    _validate_data(admin_data)

    password_hash = bcrypt.hashpw(
        admin_data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    with get_session() as session:

        admin = Admin(
            name = admin_data["name"],
            surname = admin_data["surname"],
            email = admin_data["email"],
            password = password_hash
        )

        if account_repository.check_used_email(session,admin) is not None:
            raise AppException("Esiste gia un utente con questa email", 409)
        
        return admin_repository.create(session,admin)

    

def _validate_data(admin_data):
    for field in ["name","surname","email","password"]:
        if field not in admin_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if admin_data.get(field) is None or len(admin_data[field].strip()) == 0 or len(admin_data[field]) > 30:
            raise AppException(f"Il campo {field} ha un valore non valido",400)
        
    for field in ["name", "surname"]:
        if len(admin_data[field].strip()) < 3:
            raise AppException(f"Il campo {field} deve avere almeno 3 caratteri",400)

    email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(email_pattern,admin_data["email"]):
        raise AppException("Email non valida!",400)
    
    password_pattern = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])[^ ]{8,}"
    if not re.fullmatch(password_pattern,admin_data["password"]):
        raise AppException("Password non valida!",400)          



        

    

        
    
        

