from persistence.db_config import get_session
from repository import account_repository, user_repository
from exception.app_exception import AppException
from model.user_model import User
import re
import bcrypt

def get_by_id(user_id):
    with get_session() as session:

        user = user_repository.get_by_id(session,user_id)

        if user is None:
            raise AppException("Nessun utente trovato",404)

        return user

def create(user_data):
    _validate_data(user_data)

    password_hash = bcrypt.hashpw(
        user_data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    with get_session() as session:

        user = User(
            name = user_data["name"],
            surname = user_data["surname"],
            email = user_data["email"],
            password = password_hash
        )

        if account_repository.check_used_email(session,user) is not None:
            raise AppException("Esiste gia un utente con questa email", 409)
        
        return user_repository.create(session,user)
    

def add_package(user_id,package_id):
    with get_session() as session:

        package_added = user_repository.add_package(session,user_id,package_id)

        if package_added is 0:
            raise AppException("Non è stato trovato nessun utente",404)    
        if package_added is 1:
            raise AppException("Non è stato trovato il pacco da assegnare",404)
        if package_added is 2:
            raise AppException("Il pacco è gia assegnato all'utente!",404)      
        
        return package_added
    

def _validate_data(user_data):
    for field in ["name","surname","email","password"]:
        if field not in user_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if user_data.get(field) is None or len(user_data[field].strip()) == 0 or len(user_data[field]) > 30:
            raise AppException(f"Il campo {field} ha un valore non valido",400)
        
    for field in ["name", "surname"]:
        if len(user_data[field].strip()) < 3:
            raise AppException(f"Il campo {field} deve avere almeno 3 caratteri",400)

    email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(email_pattern,user_data["email"]):
        raise AppException("Email non valida!",400)
    
    password_pattern = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])[^ ]{8,}"
    if not re.fullmatch(password_pattern,user_data["password"]):
        raise AppException("Password non valida!",400)          
