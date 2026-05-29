from repository import package_repository
from model.package_model import Package
from persistence.db_config import get_session
from exception.app_exception import AppException

def get_by_id(package_id):
    with get_session() as session:

        package = package_repository.get_by_id(session,package_id)

        if package is None:
            raise AppException("Nessun pacco trovato",404)

        return package
    
def get_all():
    with get_session() as session:
        return package_repository.get_all(session)
    
def create(package_data):
    _validate_data(package_data)

    with get_session() as session:

        package = Package(
            id = package_data["id"],
            price = package_data["price"],
            weight = package_data["weight"],
            sender_name = package_data["sender_name"],
            sender_surname = package_data["sender_surname"],
            sender_cap = package_data["sender_cap"],
            receiver_name = package_data["receiver_name"],
            receiver_surname = package_data["receiver_surname"],
            recevier_cap = package_data["recevier_cap"],
            estimated_arrival_date = package_data["estimated_arrival_date"],
            courier_id = package_data["courier_id"]          
        )

        if package_repository.check_used_id(session,package) is not None:
            raise AppException("Esiste gia un pacco con questo id")

        return package_repository.create(session,package)
    
def delete_by_id(package_id):
    with get_session() as session:

        is_deleted = package_repository.delete_by_id(session,package_id)

        if is_deleted is False:
            raise AppException("Pacco non trovato!",404)
        
        return True

def add_status(package_id,status_id):
    with get_session() as session:

        is_status_added = package_repository.add_status(session,package_id,status_id)
    
        if is_status_added is False:
            raise AppException("Non è stato possibile aggiungere il pacco all'utente",404)
        
        return True
        

def _validate_data(package_data):

    for field in ["id","price","weight","sender_name","sender_surname","sender_cap","receiver_name","receiver_surname","receiver_cap","estimated_arriaval_date","courier_id"]:
        if field not in package_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if package_data.get(field) is None or len(package_data[field].strip()) == 0:
            raise AppException(f"Il campo {field} non è valido",400)
        
        if len(package_data["id"].strip()) != 10:
            raise AppException("Il codice del pacco deve essre lungo 10 caratteri",400)

        for field in ["sender_name","sender_surname","receiver_name","receiver_surname"]:
            if len(package_data[field]) > 30:
                raise AppException(f"il campo {field} deve avere massimo 30 caratteri",400)
            if len(package_data[field].strip()) < 3:
                raise AppException(f"il campo {field} deve avere almeno 3 caratteri",400)
            
        for field in ["sender_cap","receiver_cap"]:
            if len(package_data[field]) != 5:
                raise AppException(f"il campo {field} deve avere 5 caratteri",400)
            
        for field in ["price","weight"]:
            if type(package_data[field]) is not float or type(package_data[field]) is not int:
                raise AppException(f"Il campo {field} deve essere un numero",400)
            if package_data[field] < 0:
                raise AppException(f"Il campo {field} richeide un valore positivo",400)

        if package_data["price"] >= 1000000:
            raise AppException(f"Il campo price non puo superare il valore di 1.000.000 ")
        
        if package_data["weight"] >= 1000:
            raise AppException(f"Il campo weight non puo superare il valore di 10000")

        if len(package_data["estimated_arrival_date"]) > 10:
            raise AppException("La data di arrivo stimata deve avere massimo 10 caratteri")
        
