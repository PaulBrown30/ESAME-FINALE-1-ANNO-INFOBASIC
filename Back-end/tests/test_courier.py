import unittest
from model.courier_model import Courier
from service import courier_service
from exception.app_exception import AppException
from persistence.db_config import db_init
import bcrypt


class TestCourier(unittest.TestCase):

    #Setup si avvia a ogni singola funzione
    def setUp(self):
        db_init()

    #Test dati perfetti
    def test_create_object_courier(self):
        c = Courier(name = "Paolo", surname = "marrone", email= "paolo@gmail.com", password = "SuperCiao1234.",
                    phone_number = "1234567890",birth_date = "11/01/2001", current_cap = "65124")
        self.assertEqual(c.name, "Paolo")
        self.assertEqual(c.surname, "marrone")
        self.assertEqual(c.email, "paolo@gmail.com")
        self.assertEqual(c.password, "SuperCiao1234.")
        self.assertEqual(c.phone_number, "1234567890")
        self.assertEqual(c.birth_date, "11/01/2001")
        self.assertEqual(c.current_cap, "65124")
        self.assertEqual(c.account_type, "courier")
        self.assertEqual(c.packages, [])

    #Test creazione Corriere
    def test_create_courier(self):

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
        self.assertEqual(c.id, 1)
        self.assertEqual(c.name, "Paolo")
        self.assertEqual(c.surname, "Marrone")
        password_valida = bcrypt.checkpw(
            valid_courier_data["password"].encode("utf-8"), c.password.encode("utf-8")
        )      
        self.assertEqual(password_valida, True)
        self.assertEqual(c.email, "paolo@gmail.com")
        self.assertEqual(c.phone_number, "1234567890")
        self.assertEqual(c.birth_date, "11/01/2001")
        self.assertEqual(c.current_cap, "65124")
        self.assertEqual(c.account_type, "courier")
        self.assertEqual(c.packages, [])    

    #Test id gia usato
    def test_create_courier_used_id(self):

        with self.assertRaises(AppException) as context:

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

        self.assertEqual(str(context.exception),"Esiste gia un utente con questa email")

    #Test nome gia usato
    def test_create_courier_used_phone_number(self):

        with self.assertRaises(AppException) as context:

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

            valid_courier_data = {
                "name" :"Paolo",
                "surname" : "Marrone",
                "email": "paoloss@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Esiste gia un corriere con questo numero")

    #Test nome non presente
    def test_create_courier_no_name(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "surname" : "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo name non è presente")

    #Test nome non valido
    def test_create_courier_not_valid_name(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "",
                "surname" : "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo name ha un valore non valido")

    #Test nome corto
    def test_create_courier_short_name(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "qq",
                "surname" : "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo name deve avere almeno 3 caratteri")

    #Test cognome non presente
    def test_create_courier_no_surname(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "paolo",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo surname non è presente")

    #Test cognome non valido
    def test_create_courier_not_valid_surname(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname" : "",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo surname ha un valore non valido")

    #Test cognome corto
    def test_create_courier_short_surname(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname" : "qq",
                "email": "paolo@gmail.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo surname deve avere almeno 3 caratteri")

    #Test email non presente
    def test_create_courier_no_email(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "paolo",
                "surname": "Marrone",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo email non è presente")

    #Test email non valido
    def test_create_courier_not_valid_email(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo email ha un valore non valido")

    #Test email non segue il pattern
    def test_create_courier_wrong_pattern_email(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "ciao.com",
                "password": "SuperCiao1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Email non valida!")

    #Test password non presente
    def test_create_courier_no_password(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo password non è presente")

    #Test password non valido
    def test_create_courier_not_valid_password(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo password ha un valore non valido")

    #Test password non segue il pattern
    def test_create_courier_wrong_pattern_password(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test password non segue il pattern
    def test_create_courier_wrong_pattern_password_2(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "SuperCiao11",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test password non segue il pattern
    def test_create_courier_wrong_pattern_password_3(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "superiao11.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test password non segue il pattern
    def test_create_courier_wrong_pattern_password_4(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Suo11.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test phone_number non presente
    def test_create_courier_no_phone_number(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo phone_number non è presente")

    #Test phone number non valido
    def test_create_courier_not_phone_number(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo phone_number ha un valore non valido")

    #Test phone number corta
    def test_create_courier_short_phone_number(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "123",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il numero di telefono deve avere 10 caratteri")

    #Test phone number corta
    def test_create_courier_long_phone_number(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "12345678901",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il numero di telefono deve avere 10 caratteri")

    #Test password non segue il pattern
    def test_create_courier_wrong_pattern_password_4(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Suo11.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Password non valida!")

    #Test birth date non presente
    def test_create_courier_no_birth_date(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo birth_date non è presente")

    #Test birth date non valida
    def test_create_courier_not_birth_date(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il campo birth_date ha un valore non valido")

    #Test birth date anno non valido
    def test_create_courier_birth_date_wrong_year_1(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "201-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"L'anno deve avere 4 cifre")

    #Test birth date -> non maggiorenne
    def test_create_courier_birth_date_not_18(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2011-01-11",
                "current_cap": "65124",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il corriere deve avere piu di 18 anni")

    #Test longer CAP
    def test_create_courier_longer_CAP(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "651222",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il Cap corrente deve avere 5 caratteri")

    #Test shorter CAP
    def test_create_courier_shorter_CAP(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "6512",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il Cap corrente deve avere 5 caratteri")

    #Test CAP with non numbers
    def test_create_courier_shorter_CAP(self):

        with self.assertRaises(AppException) as context:

            valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "6512s",
                }
            c = courier_service.create(valid_courier_data)

        self.assertEqual(str(context.exception),"Il Cap corrente deve essere numerico")

    #Test get by id
    def test_get_by_id(self):

        valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }
        
        status = courier_service.create(valid_courier_data)

        c  = courier_service.get_by_id(1)

        self.assertEqual(c.id, 1)
        self.assertEqual(c.name, "Paolo")
        self.assertEqual(c.surname, "Marrone")
        password_valida = bcrypt.checkpw(
            valid_courier_data["password"].encode("utf-8"), c.password.encode("utf-8")
        )      
        self.assertEqual(password_valida, True)
        self.assertEqual(c.email, "paolo@gmail.com")
        self.assertEqual(c.phone_number, "1234567890")
        self.assertEqual(c.birth_date, "11/01/2001")
        self.assertEqual(c.current_cap, "65124")
        self.assertEqual(c.account_type, "courier")
        self.assertEqual(c.packages, [])   

    #Test get by non existing id
    def test_get_by_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            s = courier_service.get_by_id(1)

        self.assertEqual(str(context.exception),"Nessun corriere trovato")

    #Test get all no elements
    def test_get_all(self):

        s = courier_service.get_all()
        self.assertEqual(len(s),0)

    #Test get all with elements
    def test_get_all_with_elements(self):

        valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }        
        status = courier_service.create(valid_courier_data)

        valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo1@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567820",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }        
        status = courier_service.create(valid_courier_data)

        s = courier_service.get_all()
        self.assertEqual(len(s),2)
        self.assertEqual(s[0].id,1)
        self.assertEqual(s[1].id,2)

    #Test update cap
    def test_update_current_cap(self):

        valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }        
        status = courier_service.create(valid_courier_data)

        updated_courier = courier_service.update_current_cap(1,"65125")
        self.assertEqual(updated_courier.current_cap,"65125")

    #Test delete 
    def test_delete(self):

        valid_courier_data = {
                "name": "Paolo",
                "surname": "Marrone",
                "email": "paolo@gmail.com",
                "password": "Superpaolo1234.",
                "phone_number": "1234567890",
                "birth_date": "2001-01-11",
                "current_cap": "65124",
                }        
        status = courier_service.create(valid_courier_data)

        deleted = courier_service.delete_by_id(1)
        self.assertEqual(deleted,True)