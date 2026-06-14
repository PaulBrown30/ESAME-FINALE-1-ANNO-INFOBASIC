from repository import status_repository
from model.status_model import Status
from persistence.db_config import get_session
from exception.app_exception import AppException


def get_by_id(status_id):
    with get_session() as session:

        status = status_repository.get_by_id(session,status_id)

        if status is None:
            raise AppException("Stato non trovato",404)
        
        return status

def get_all():
    with get_session() as session:

        return status_repository.get_all(session)

def create(status_data):
    _validate_data(status_data)

    with get_session() as session:

        status = Status(
            id = status_data["id"],
            name = status_data["name"],
            description = status_data["description"]
        )

        if status_repository.check_used_id(session,status) is not None:
            raise AppException("Esiste gia uno stato con questo id",409)

        if status_repository.check_used_name(session,status) is not None:
            raise AppException("Esiste gia uno stato con questo nome",409)
        
        return status_repository.create(session,status)

    
def add_ammitted_transition(existing_status_id,added_status_id):
    
    with get_session() as session:
        
        existing_status = status_repository.get_by_id(session, existing_status_id)
        if existing_status is None:
            raise AppException("Stato di partenza non trovato", 404)

        added_status = status_repository.get_by_id(session, added_status_id)
        if added_status is None:
            raise AppException("Stato di arrivo non trovato", 404)
        
        is_transition_added = status_repository.add_status_transitions(session,existing_status,added_status)
        if is_transition_added is False:
            raise AppException("Questa transizione gia esiste", 404)
        
        return True
    
def _validate_data(status_data):
    for field in ["id","name","description"]:
        if field not in status_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if status_data.get(field) is None or len(status_data[field].strip()) == 0:
            raise AppException(f"Il campo {field} non è valido",400)
    
    if len(status_data["id"]) > 5:
        raise AppException("L'id deve avere massimo 5 caratteri",400)    

    if len(status_data["name"]) > 30:
        raise AppException("Il nome deve avere massimo 30 caratteri",400)
    
    if len(status_data["description"]) > 100:
        raise AppException("La descrizione deve avere massimo 100 caratteri",400)
    
