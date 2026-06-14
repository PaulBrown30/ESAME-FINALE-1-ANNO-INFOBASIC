import unittest
from model.user_model import User
from service import user_service, courier_service, status_service, package_service
from exception.app_exception import AppException
from persistence.db_config import db_init
import bcrypt



class TestUser(unittest.TestCase):

    #Setup si avvia a ogni singola funzione
    def setUp(self):
        db_init()
    
    #Test dati perfetti
    def test_create_object_user(self):
        u = User(name = "Mario", surname = "Rossi", email = "mario@gmail.com", password = "Password123.")
        self.assertEqual(u.name, "Mario")
        self.assertEqual(u.surname, "Rossi")
        self.assertEqual(u.email, "mario@gmail.com")
        self.assertEqual(u.password, "Password123.")

    #Test dati perfetti
    def test_create_user(self):
        valid_user_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
        user = user_service.create(valid_user_data)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Mario")
        self.assertEqual(user.surname, "Rossi")
        self.assertEqual(user.email, "mario@gmail.com")
        password_valida = bcrypt.checkpw(
            valid_user_data["password"].encode("utf-8"), user.password.encode("utf-8")
        )      
        self.assertEqual(password_valida, True)

    #Test email gia usato
    def test_create_user_used_email(self):

        with self.assertRaises(AppException) as context:

            valid_user_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user = user_service.create(valid_user_data)

            invalid_user_data = {"name" : "Luigi","surname" :"Bianchi", "email" : "mario@gmail.com", "password" : "AltraPassword123."}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Esiste gia un utente con questa email")

    #Test name non presente
    def test_repository_create_user_name_not_existing(self):

        with self.assertRaises(AppException) as context:

            invalid_user_data = {"surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Il campo name non è presente")

    #Test name vuoto
    def test_repository_create_user_name_empty(self):

        with self.assertRaises(AppException) as context:

            invalid_user_data = {"name" : "","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Il campo name ha un valore non valido")

    #Test name lungo
    def test_repository_create_user_name_too_long(self):

        with self.assertRaises(AppException) as context:

            invalid_user_data = {"name" : "Marioooooooooooooooooooooooooooooooooooooooooo", "surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Il campo name ha un valore non valido")

    #Test name corto
    def test_repository_create_user_name_too_short(self):

        with self.assertRaises(AppException) as context:

            invalid_user_data = {"name" : "Ma", "surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Il campo name deve avere almeno 3 caratteri")

    #Test email non valida
    def test_repository_create_user_email_invalid(self):

        with self.assertRaises(AppException) as context:

            invalid_user_data = {"name" : "Mario", "surname" :"Rossi", "email" : "://gmail.com", "password" : "SuperPassword123."}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Email non valida!")

    #Test password non valida
    def test_repository_create_user_password_invalid(self):

        with self.assertRaises(AppException) as context:

            invalid_user_data = {"name" : "Mario", "surname" :"Rossi", "email" : "mario@gmail.com", "password" : "123"}
            user_service.create(invalid_user_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test get by id
    def test_get_by_id(self):

        valid_user_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
        user = user_service.create(valid_user_data)

        u = user_service.get_by_id(1)
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, "Mario")
        self.assertEqual(u.email, "mario@gmail.com")

    #Test get by non existing id
    def test_get_by_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            u = user_service.get_by_id(999)

        self.assertEqual(str(context.exception),"Nessun utente trovato")

    #Test add package
    def test_add_package(self):


        valid_status_data = {
            "id": "S-001", 
            "name": "Preso in carico", 
            "description": "Pacco preso in carico"
        }
        status_service.create(valid_status_data)
        
        valid_courier_data = {
            "name": "Paolo",
            "surname": "Marrone",
            "email": "paolo@gmail.com",
            "password": "SuperCiao1234.",
            "phone_number": "1234567890",
            "birth_date": "2001-01-11",
            "current_cap": "65124"
        }
        courier_service.create(valid_courier_data)

        valid_user_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
        user = user_service.create(valid_user_data)

        valid_package_data = {
            "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
            "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
        }
        package = package_service.create(valid_package_data)

        package_added = user_service.add_package(2, "1234567890")
        self.assertEqual(package_added.id, "1234567890")

    #Test add package non existing user
    def test_add_package_non_existing_user(self):

        with self.assertRaises(AppException) as context:

            valid_status_data = {
                "id": "S-001", 
                "name": "Preso in carico", 
                "description": "Pacco preso in carico"
            }
            status_service.create(valid_status_data)
            
            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124"
            }
            courier_service.create(valid_courier_data)

            valid_package_data = {
                "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
                "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
            }
            package = package_service.create(valid_package_data)

            user_service.add_package(999, "1234567890")

        self.assertEqual(str(context.exception),"Non è stato trovato nessun utente")

    #Test add package non existing package
    def test_add_package_non_existing_package(self):

        with self.assertRaises(AppException) as context:

            valid_user_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user = user_service.create(valid_user_data)

            user_service.add_package(1, "P999999999")

        self.assertEqual(str(context.exception),"Non è stato trovato il pacco da assegnare")

    #Test add package already assigned
    def test_add_package_already_assigned(self):

        with self.assertRaises(AppException) as context:

            valid_user_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            user = user_service.create(valid_user_data)

            valid_status_data = {
                "id": "S-001", 
                "name": "Preso in carico", 
                "description": "Pacco preso in carico"
            }
            status_service.create(valid_status_data)
            
            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124"
            }
            courier_service.create(valid_courier_data)

            valid_package_data = {
                "id" : "1234567890", "weight" : 41, "sender_name" : "gino", "sender_surname" : "giallo",
                "sender_cap" : "65124", "receiver_name" : "Andrea", "receiver_surname" : "Viola", "receiver_cap" : "00187"
            }
            package = package_service.create(valid_package_data)

            user_service.add_package(1, "1234567890")
            user_service.add_package(1, "1234567890")

        self.assertEqual(str(context.exception),"Il pacco è gia assegnato all'utente!")