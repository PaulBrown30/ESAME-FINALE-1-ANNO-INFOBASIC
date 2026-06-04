from persistence.db_config import get_session
from repository import account_repository, courier_repository
from exception.app_exception import AppException
from model.courier_model import Courier
import re
import bcrypt

def get_by_id(courier_id):
    with get_session() as session:

        courier = courier_repository.get_by_id(session,courier_id)

        if courier is None:
            raise AppException("Nessun corriere trovato",404)

        return courier
    
def get_all():
    with get_session() as session:
        return courier_repository.get_all(session)
    
def get_available_couriers():
    with get_session() as session:
        return courier_repository.get_available_couriers(session)

def create(courier_data):
    _validate_data(courier_data)

    password_hash = bcrypt.hashpw(
        courier_data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    with get_session() as session:

        courier = Courier(
            name = courier_data["name"],
            surname = courier_data["surname"],
            email = courier_data["email"],
            password = password_hash,
            phone_number = courier_data["phone_number"],
            max_load = courier_data["max_load"],
            birth_date = courier_data["birth_date"]
        )

        if account_repository.check_used_email(session,courier) is not None:
            raise AppException("Esiste gia un utente con questa email", 409)

        if courier_repository.check_used_phone_number(session,courier) is not None:
            raise AppException("Esiste gia un corriere con questo numero", 409)   

        return courier_repository.create(session,courier)

def update(courier_id,courier_data):
    _validate_data(courier_data)

    password_hash = bcrypt.hashpw(
        courier_data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    with get_session() as session:
        courier = Courier(
            id = courier_id,
            name = courier_data["name"],
            surname = courier_data["surname"],
            email = courier_data["email"],
            password = password_hash,
            phone_number = courier_data["phone_number"],
            max_load = courier_data["max_load"],
            birth_date = courier_data["birth_date"]
        )

        if account_repository.check_used_email(session,courier) is not None:
            raise AppException("Esiste gia un utente con questa email", 409)
        
        if courier_repository.check_used_phone_number(session,courier) is not None:
            raise AppException("Esiste gia un corriere con questo numero", 409)            
        
        return courier_repository.update(session,courier)
    
def delete_by_id(courier_id):
    with get_session() as session:

        is_deleted = courier_repository.delete_by_id(session,courier_id)

        if is_deleted is False:
            raise AppException("Corriere non trovato!",404)
        
        return True

def _validate_data(courier_data):
    for field in ["name","surname","email","password","phone_number","birth_date"]:
        if field not in courier_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if courier_data.get(field) is None or len(courier_data[field].strip()) == 0 or len(courier_data[field]) > 30:
            raise AppException(f"Il campo {field} ha un valore non valido",400)
        
    if "max_load" not in courier_data:
            raise AppException(f"Il campo max_load non è presente",400)
    if courier_data.get("max_load") is None:
        raise AppException(f"Il campo {field} ha un valore non valido",400)
    
    for field in ["name", "surname"]: 
        if len(courier_data[field].strip()) < 3:
            raise AppException(f"Il campo {field} deve avere almeno 3 caratteri",400)

    email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(email_pattern,courier_data["email"]):
        raise AppException("Email non valida!",400)
    
    password_pattern = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{8,}$"
    if not re.fullmatch(password_pattern,courier_data["password"]):
        raise AppException("Password non valida!",400)          
    
    if len(courier_data["phone_number"]) != 10:
        raise AppException("Il numero di telefono deve avere 10 caratteri",400)
    
    if type(courier_data["max_load"]) != int or courier_data["max_load"] < 0:
        raise AppException("Il carico massimo non è valido",400)
    
    if len(courier_data["birth_date"]) > 10:
        raise AppException("La data di nascita deve avere meno di 10 caratteri",400)
    



    

    


