import unittest
from model.package_model import Package
from service import package_service, courier_service,status_service
from exception.app_exception import AppException
from persistence.db_config import db_init
import datetime
import pgeocode
from geopy.distance import geodesic



class TestPackage(unittest.TestCase):

    #Setup si avvia a ogni singola funzione
    def setUp(self):
        db_init()
        valid_courier_data = {
            "name" :"Paolo",
            "surname" : "Marrone",
            "email": "paolo@gmail.com",
            "password": "SuperCiao1234.",
            "phone_number": "1234567890",
            "birth_date": "2001-01-11",
            "current_cap": "65124",
            }
        c = courier_service.create(valid_courier_data)

        valid_status_data = {"id" : "S-001","name" :"test 1", "description" : "descrizione test 1"}
        s = status_service.create(valid_status_data)


    #Test dati perfetti
    def test_create_object_package(self):
        p = Package(id = "1234567890", price = "41", weight = "41",sender_name = "gino", sender_surname=  "giallo",
                    sender_cap = "65124",receiver_name = "Andrea", receiver_surname = "Viola", receiver_cap = "65125",
                    estimated_arrival_date = "1",actual_arrival_date = "1",courier_id = 1,
                    active = False
                    )
        self.assertEqual(p.id, "1234567890")
        self.assertEqual(p.price, "41")
        self.assertEqual(p.weight, "41")
        self.assertEqual(p.sender_name, "gino")
        self.assertEqual(p.sender_surname, "giallo")
        self.assertEqual(p.sender_cap, "65124")
        self.assertEqual(p.receiver_name, "Andrea")
        self.assertEqual(p.receiver_surname, "Viola")
        self.assertEqual(p.receiver_cap, "65125")
        self.assertEqual(p.estimated_arrival_date, "1")
        self.assertEqual(p.actual_arrival_date, "1")
        self.assertEqual(p.courier_id, 1)
        self.assertEqual(p.active, False)

    #Test dati perfetti
    def test_create_package(self):
        valid_package_data = {"id" : "1234567890", "weight" : 41,"sender_name" : "gino", "sender_surname" : "giallo",
                    "sender_cap" : "65124","receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00151",
                    }
                    
        p = package_service.create(valid_package_data)

        city_name = pgeocode.Nominatim('it')
        info_cap1 = city_name.query_postal_code("65124")
        info_cap2 = city_name.query_postal_code("00151")
        
        distance = geodesic((info_cap1['latitude'], info_cap1['longitude']), (info_cap2['latitude'], info_cap2['longitude'])).km
        time_to_add = datetime.timedelta(days=(distance / 60.0) / 24)
        
        expected_delivery_date = (p.estimated_arrival_date - time_to_add) + time_to_add

        expected_price = (distance * 41.0) / 1000

        self.assertEqual(p.id, "1234567890")
        self.assertAlmostEqual(float(p.price), float(expected_price),places=2)
        self.assertEqual(p.weight, 41.0)
        self.assertEqual(p.sender_name, "gino")
        self.assertEqual(p.sender_surname, "giallo")
        self.assertEqual(p.sender_cap, "65124")
        self.assertEqual(p.receiver_name, "Andrea")
        self.assertEqual(p.receiver_surname, "Viola")
        self.assertEqual(p.receiver_cap, "00151")
        self.assertEqual(p.estimated_arrival_date, expected_delivery_date)
        self.assertEqual(p.actual_arrival_date, None)
        self.assertEqual(p.courier_id, 1)
        self.assertEqual(p.active, True)

    # Test id non presente
    def test_repository_create_package_id_not_existing(self):
        with self.assertRaises(AppException) as context:

            invalid_package_data = {
                "weight": 41, "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)

        self.assertEqual(str(context.exception), "Il campo id non è presente")

    # Test id vuoto
    def test_repository_create_package_id_empty(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "", "weight": 41, "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il campo id non è valido")

    # Test id lunghezza errata (diverso da 10)
    def test_repository_create_package_id_wrong_length(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "12345", "weight": 41, "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il codice del pacco deve essre lungo 10 caratteri")

    # Test sender_name non presente
    def test_repository_create_package_sender_name_not_existing(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": 41, "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il campo sender_name non è presente")

    # Test sender_name vuoto
    def test_repository_create_package_sender_name_empty(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": 41, "sender_name": "   ", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il campo sender_name non è valido")

    # Test sender_name troppo corto 
    def test_repository_create_package_sender_name_too_short(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": 41, "sender_name": "gi", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "il campo sender_name deve avere almeno 3 caratteri")

    # Test sender_name troppo lungo 
    def test_repository_create_package_sender_name_too_long(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": 41, 
                "sender_name": "ginoooooooooooooooooooooooooooooooooooooooooo", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "il campo sender_name deve avere massimo 30 caratteri")

    # Test sender_cap lunghezza errata
    def test_repository_create_package_sender_cap_wrong_length(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": 41, "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "651", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "il campo sender_cap deve avere 5 caratteri")

    # Test weight non presente
    def test_repository_create_package_weight_not_existing(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il campo weight non è presente")

    # Test weight negativo
    def test_repository_create_package_weight_negative(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": -5, "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il campo weight richeide un valore positivo")

    # Test weight troppo alto (maggiore o uguale a 1000)
    def test_repository_create_package_weight_too_high(self):
        with self.assertRaises(AppException) as context:
            invalid_package_data = {
                "id": "1234567890", "weight": 1050, "sender_name": "gino", "sender_surname": "giallo",
                "sender_cap": "65124", "receiver_name": "Andrea", "receiver_surname": "Viola", "receiver_cap": "00187"
            }
            package_service.create(invalid_package_data)
        self.assertEqual(str(context.exception), "Il campo weight non puo superare il valore di 1000")

    #Test get by id
    def test_get_by_id(self):

        valid_package_data = {
            "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
            "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
        }
        package = package_service.create(valid_package_data)

        p = package_service.get_by_id("1234567890")
        self.assertEqual(p.id, "1234567890")
        self.assertEqual(p.sender_name, "gino")
        self.assertEqual(p.receiver_name, "Andrea")

    #Test get by non existing id
    def test_get_by_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            p = package_service.get_by_id("1234567890")

        self.assertEqual(str(context.exception),"Nessun pacco trovato")

    #Test get all no elements
    def test_get_all(self):

        p = package_service.get_all()
        self.assertEqual(len(p),0)

    #Test get all with elements
    def test_get_all_with_elements(self):

        valid_package_data = {
            "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
            "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
        }
        package_service.create(valid_package_data)
        
        valid_package_data_2 = {
            "id" : "0987654321", "weight" : 20, "sender_name" : "mario", "sender_surname" : "rossi",
            "sender_cap" : "65124", "receiver_name" : "luca", "receiver_surname" : "bianchi", "receiver_cap" : "00187"
        }
        package_service.create(valid_package_data_2)

        p = package_service.get_all()
        self.assertEqual(len(p),2)
        self.assertEqual(p[0].id,"1234567890")
        self.assertEqual(p[0].sender_name,"gino")
        self.assertEqual(p[1].id,"0987654321")
        self.assertEqual(p[1].sender_name,"mario")

    #Test delete 
    def test_delete(self):

        valid_package_data = {
            "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
            "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
        }
        package = package_service.create(valid_package_data)

        deleted = package_service.delete_by_id("1234567890")
        self.assertEqual(deleted,True)

    #Test delete non existing id
    def test_delete_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            package_service.delete_by_id("1234567890")

        self.assertEqual(str(context.exception),"Pacco non trovato!")

    #Test set inactive
    def test_set_inactive(self):

        valid_package_data = {
            "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
            "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
        }
        package = package_service.create(valid_package_data)

        inactive = package_service.set_inactive("1234567890")
        self.assertEqual(inactive,True)

    #Test set inactive non existing id
    def test_set_inactive_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            package_service.set_inactive("1234567890")

        self.assertEqual(str(context.exception),"Pacco non trovato!")

    #Test set inactive already inactive
    def test_set_inactive_already_inactive(self):

        with self.assertRaises(AppException) as context:

            valid_package_data = {
                "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
                "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
            }
            package = package_service.create(valid_package_data)
                        
            package_service.set_inactive("1234567890")
            package_service.set_inactive("1234567890")

        self.assertEqual(str(context.exception),"Il Pacco è gia inattivo!")

    #Test set arrival date
    def test_set_arrival_date(self):

        valid_package_data = {
            "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
            "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
        }
        package = package_service.create(valid_package_data)

        date_setted = package_service.set_arrival_date("1234567890")
        self.assertEqual(date_setted,True)

    #Test set arrival date non existing id
    def test_set_arrival_date_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            package_service.set_arrival_date("1234567890")

        self.assertEqual(str(context.exception),"Pacco non trovato!")

