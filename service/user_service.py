from persistence.db_config import get_session
from repository import account_repository, user_repository
from exception.app_exception import AppException
from model.user_model import User
import re


def get_by_id(user_id):
    with get_session() as session:

        user = user_repository.get_by_id(session,user_id)

        if user is None:
            raise AppException("Nessun utente trovato",404)

        return user

def create(user_data):
    _validate_data(user_data)

    with get_session() as session:

        user = User(
            name = user_data["name"],
            surname = user_data["surname"],
            email = user_data["email"],
            password = user_data["password"]
        )

        if account_repository.check_used_email(session,user) is not None:
            raise AppException("Esiste gia un utente con questa email", 409)
        
        return user_repository.create(session,user)
    

def add_package(user_id,package_id):
    with get_session() as session:

        is_package_added = user_repository.add_package(session,user_id,package_id["package_id"])
    
        if is_package_added is False:
            raise AppException("Non è stato possibile aggiungere il pacco all'utente",404)
        
        return True
    

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
    
    password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$"
    if not re.fullmatch(password_pattern,user_data["password"]):
        raise AppException("Password non valida!",400)          
