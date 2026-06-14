import unittest
from model.admin_model import Admin
from service import admin_service
from exception.app_exception import AppException
from persistence.db_config import db_init
import bcrypt


class TestAdmin(unittest.TestCase):

    #Setup si avvia a ogni singola funzione
    def setUp(self):
        db_init()
    
    #Test dati perfetti
    def test_create_object_admin(self):
        a = Admin(name = "Mario", surname = "Rossi", email = "mario@gmail.com", password = "Password123.")
        self.assertEqual(a.name, "Mario")
        self.assertEqual(a.surname, "Rossi")
        self.assertEqual(a.email, "mario@gmail.com")
        self.assertEqual(a.password, "Password123.")

    #Test dati perfetti
    def test_create_admin(self):
        valid_admin_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
        admin = admin_service.create(valid_admin_data)
        self.assertEqual(admin.id, 1)
        self.assertEqual(admin.name, "Mario")
        self.assertEqual(admin.surname, "Rossi")
        self.assertEqual(admin.email, "mario@gmail.com")
        password_valida = bcrypt.checkpw(
            valid_admin_data["password"].encode("utf-8"), admin.password.encode("utf-8")
        )      
        self.assertEqual(password_valida, True)

    #Test email gia usato
    def test_create_admin_used_email(self):

        with self.assertRaises(AppException) as context:

            valid_admin_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            admin = admin_service.create(valid_admin_data)

            invalid_admin_data = {"name" : "Luigi","surname" :"Bianchi", "email" : "mario@gmail.com", "password" : "AltraPassword123."}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Esiste gia un utente con questa email")

    #Test name non presente
    def test_repository_create_admin_name_not_existing(self):

        with self.assertRaises(AppException) as context:

            invalid_admin_data = {"surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Il campo name non è presente")

    #Test name vuoto
    def test_repository_create_admin_name_empty(self):

        with self.assertRaises(AppException) as context:

            invalid_admin_data = {"name" : "","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Il campo name ha un valore non valido")

    #Test name lungo
    def test_repository_create_admin_name_too_long(self):

        with self.assertRaises(AppException) as context:

            invalid_admin_data = {"name" : "Marioooooooooooooooooooooooooooooooooooooooooo", "surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Il campo name ha un valore non valido")

    #Test name corto
    def test_repository_create_admin_name_too_short(self):

        with self.assertRaises(AppException) as context:

            invalid_admin_data = {"name" : "Ma", "surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Il campo name deve avere almeno 3 caratteri")

    #Test email non valida
    def test_repository_create_admin_email_invalid(self):

        with self.assertRaises(AppException) as context:

            invalid_admin_data = {"name" : "Mario", "surname" :"Rossi", "email" : "paologmail.com", "password" : "SuperPassword123."}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Email non valida!")

    #Test password non valida
    def test_repository_create_admin_password_invalid(self):

        with self.assertRaises(AppException) as context:

            invalid_admin_data = {"name" : "Mario", "surname" :"Rossi", "email" : "mario@gmail.com", "password" : "123"}
            admin_service.create(invalid_admin_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test get by id
    def test_get_by_id(self):

        valid_admin_data = {"name" : "Mario","surname" :"Rossi", "email" : "mario@gmail.com", "password" : "SuperPassword123."}
        admin = admin_service.create(valid_admin_data)

        a = admin_service.get_by_id(1)
        self.assertEqual(a.id, 1)
        self.assertEqual(a.name, "Mario")
        self.assertEqual(a.email, "mario@gmail.com")

    #Test get by non existing id
    def test_get_by_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            a = admin_service.get_by_id(1)

        self.assertEqual(str(context.exception),"Nessun admin trovato")
    