from repository import package_repository
from repository import courier_repository
from model.package_model import Package
from service import courier_service
from persistence.db_config import get_session
from exception.app_exception import AppException
import pgeocode
from geopy.distance import geodesic
import datetime

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

    package_data["weight"] = float(package_data["weight"])

    with get_session() as session:
        
        less_package_courier = courier_repository.get_less_packages_courier(session)

        if less_package_courier is None:
            raise AppException("Nessun corriere trovato",404)
        
        nomi_paese = pgeocode.Nominatim('it')

        cap1 = package_data["sender_cap"]
        cap2 = package_data["receiver_cap"]


        info_cap1 = nomi_paese.query_postal_code(cap1)
        info_cap2 = nomi_paese.query_postal_code(cap2)

        # è tutto normale davide, sto controllando l'esistenza dei CAP confrontando due valori dell'oggetto creato
        # (sono NaN se non esiste il CAP, e i Nan sono sempre diversi tra loro)
        test_cap1 = nomi_paese.query_postal_code(cap1)
        test_cap2 = nomi_paese.query_postal_code(cap2)

        if info_cap1["latitude"] != test_cap1["latitude"]:
            raise AppException("Il Cap del mittente non è valido",400)
        if info_cap2["latitude"] != test_cap2["latitude"]:
            raise AppException("Il Cap del destinatario non è valido",400)            

        coordinate1 = (info_cap1['latitude'], info_cap1['longitude'])
        coordinate2 = (info_cap2['latitude'], info_cap2['longitude'])

        if less_package_courier.packages != []:
            cap3 = less_package_courier.packages[-1].receiver_cap
            info_cap3 = nomi_paese.query_postal_code(cap3)
            coordinate3 = (info_cap3['latitude'], info_cap3['longitude'])
            distance = geodesic(coordinate3, coordinate1).km + geodesic(coordinate1, coordinate2).km

        else:
            distance = geodesic(coordinate1, coordinate2).km

        calculated_price = (distance * package_data["weight"])/1000
        
        # Calcolo durata del viaggio:
        AVARAGE_SPEED_KMH = 60.0

        hours = distance / AVARAGE_SPEED_KMH

        days = hours / 24

        estimated_time = days
        time_to_add = datetime.timedelta(days=estimated_time)

        if less_package_courier.packages != []:
            last_package_estimated_arrival_date = less_package_courier.packages[-1].estimated_arrival_date
            delivery_date = last_package_estimated_arrival_date + time_to_add
        else:
            today = datetime.datetime.now()
            delivery_date = today + time_to_add

        package = Package(
            id = package_data["id"],
            price = calculated_price,
            weight = package_data["weight"],
            sender_name = package_data["sender_name"],
            sender_surname = package_data["sender_surname"],
            sender_cap = package_data["sender_cap"],
            receiver_name = package_data["receiver_name"],
            receiver_surname = package_data["receiver_surname"],
            receiver_cap = package_data["receiver_cap"],
            estimated_arrival_date = delivery_date,
            courier_id = less_package_courier.id          
        )

        if package_repository.check_used_id(session,package) is not None:
            raise AppException("Esiste gia un pacco con questo id",409)

        return package_repository.create(session,package)
    
def delete_by_id(package_id):
    with get_session() as session:

        is_deleted = package_repository.delete_by_id(session,package_id)

        if is_deleted is False:
            raise AppException("Pacco non trovato!",404)
        
        return True

def add_status(package_id,status_id,courier_id):
    with get_session() as session:

        package = package_repository.add_status(session,package_id,status_id)
    
        if package is 1:
            raise AppException("Non è stato possibile trovare il pacco",404)
        
        if package is 2:
            raise AppException("Non è stato possibile trovare lo stato",404)
        
        if status_id in ["S-003","S-101","S-102","S-103"]:
            set_inactive(package_id)

        if status_id in ["S-003"]:
            set_arrival_date(package_id)

        if status_id in ["S-002","S-103"]  :          
            courier = courier_service.update_current_cap(courier_id,package.sender_cap)
        elif status_id in ["S-003","S-101"] :          
            courier = courier_service.update_current_cap(courier_id,package.receiver_cap)  
        else:
            courier = courier_service.update_current_cap(courier_id,None) 

        return courier
        
def set_inactive(package_id):
    with get_session() as session:
        
        is_inactive = package_repository.set_inactive(session,package_id)

        if is_inactive is False:
            raise AppException("Pacco non trovato!",404)
        
        return True
    
def set_arrival_date(package_id):
    with get_session() as session:
        
        is_date_setted = package_repository.set_arrival_date(session,package_id)

        if is_date_setted is False:
            raise AppException("Pacco non trovato!",404)
        
        return True
       
def _validate_data(package_data):

    for field in ["id","sender_name","sender_surname","sender_cap","receiver_name","receiver_surname","receiver_cap"]:
        if field not in package_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if package_data.get(field) is None or len(package_data[field].strip()) == 0:
            raise AppException(f"Il campo {field} non è valido",400)
        
    for field in ["weight"]:
        if field not in package_data:
            raise AppException(f"Il campo {field} non è presente",400)
        if package_data.get(field) is None:
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
        
    

    try:
        package_data["weight"] = float(package_data["weight"])

        if type(package_data["weight"]) is not float and type(package_data["weight"]) is not int:
            raise AppException(f"Il campo weight deve essere un numero",400)
        if package_data["weight"] < 0:
            raise AppException(f"Il campo weight richeide un valore positivo",400)    
        if package_data["weight"] >= 1000:
            raise AppException(f"Il campo weight non puo superare il valore di 1000",400)
    except:
        raise AppException(f"Il campo {field} deve essere un numero",400)


        
