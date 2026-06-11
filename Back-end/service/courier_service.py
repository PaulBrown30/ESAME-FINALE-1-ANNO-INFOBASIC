from persistence.db_config import get_session
from repository import account_repository, courier_repository
from exception.app_exception import AppException
from model.courier_model import Courier
import re
import bcrypt
from datetime import date

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

    dataStringa = courier_data["birth_date"]
    anno, mese, giorno = dataStringa.split("-")
    dataOrdinata = f"{giorno}/{mese}/{anno}"

    with get_session() as session:

        courier = Courier(
            name = courier_data["name"],
            surname = courier_data["surname"],
            email = courier_data["email"],
            password = password_hash,
            phone_number = courier_data["phone_number"],
            max_load = courier_data.get("max_load"),
            birth_date = dataOrdinata,
            current_cap = courier_data.get("current_cap")
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
            max_load = courier_data.get("max_load"),
            birth_date = courier_data["birth_date"],
            current_cap = courier_data.get("current_cap")
        )

        if account_repository.check_used_email(session,courier) is not None:
            raise AppException("Esiste gia un utente con questa email", 409)
        
        if courier_repository.check_used_phone_number(session,courier) is not None:
            raise AppException("Esiste gia un corriere con questo numero", 409)            
        
        return courier_repository.update(session,courier)
    
def update_current_cap(courier_id,current_cap):
    with get_session() as session:
        
        if current_cap != None:

            if len(current_cap) != 5:
                raise AppException("Il Cap corrente deve avere 5 caratteri",400)
            try:
                conversione = int(current_cap)
            except:
                raise AppException("Il Cap corrente deve essre numerico",400)

        courier = courier_repository.get_by_id(session,courier_id)

        if courier is None:
            raise AppException("Nessun corriere trovato",404)
        
        if current_cap != None:
            courier.current_cap = current_cap

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
    
    for field in ["name", "surname"]: 
        if len(courier_data[field].strip()) < 3:
            raise AppException(f"Il campo {field} deve avere almeno 3 caratteri",400)

    email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.fullmatch(email_pattern,courier_data["email"]):
        raise AppException("Email non valida!",400)
    
    password_pattern = "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])[^ ]{8,}"
    if not re.fullmatch(password_pattern,courier_data["password"]):
        raise AppException("Password non valida!",400)          
    
    if len(courier_data["phone_number"]) != 10:
        raise AppException("Il numero di telefono deve avere 10 caratteri",400)
    
    if courier_data.get("max_load") is not None:
        if type(courier_data.get("max_load")) != int or courier_data["max_load"] < 0:
            raise AppException("Il carico massimo non è valido",400)
    
    if len(courier_data["birth_date"]) > 10:
        raise AppException("La data di nascita deve avere meno di 10 caratteri",400)
    

    if courier_data.get("current_cap") is not None:    
        if len(courier_data["current_cap"]) != 5:
            raise AppException("Il Cap corrente deve avere 5 caratteri",400)
        try:
            conversione = int(courier_data["current_cap"])
        except:
            raise AppException("Il Cap corrente deve essre numerico",400)

    dataStringa = courier_data["birth_date"]
    anno, mese, giorno = dataStringa.split("-")

    if len(anno) != 4:
        raise AppException("L'anno deve avere 4 cifre",400)
    if len(mese) != 2:
        raise AppException("Il mese deve avere 2 cifre",400)
    if len(giorno) != 2:
        raise AppException("Il giorno deve avere 2 cifre",400)

    data_nascita = date(int(anno), int(mese), int(giorno))
    oggi = date.today()

    eta = oggi.year - data_nascita.year

    if eta < 18:
        raise AppException("Il corriere deve avere piu di 18 anni",400)

    


