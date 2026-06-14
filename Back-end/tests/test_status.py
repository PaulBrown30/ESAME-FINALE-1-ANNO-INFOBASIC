import unittest
from model.status_model import Status
from service import status_service
from exception.app_exception import AppException
from persistence.db_config import db_init



class TestStatus(unittest.TestCase):

    def setUp(self):
        db_init()
    


    #Test dati perfetti
    def test_create_object_status(self):
        s = Status(id = "S-001", name = "test 1", description = "descrizione test 1")
        self.assertEqual(s.id, "S-001")
        self.assertEqual(s.name, "test 1")
        self.assertEqual(s.description, "descrizione test 1")

    #Test dati perfetti
    def test_create_status(self):
        valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
        status = status_service.create(valid_status_data)
        self.assertEqual(status.id, "S-222")
        self.assertEqual(status.name, "test 1")
        self.assertEqual(status.description, "descrizione test 1")

    #Test id gia usato
    def test_create_status_used_id(self):

        with self.assertRaises(AppException) as context:

            valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
            status = status_service.create(valid_status_data)

            invalid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Esiste gia uno stato con questo id")

    #Test nome gia usato
    def test_create_status_used_name(self):

        with self.assertRaises(AppException) as context:

            valid_status_data = {"id" : "S-221","name" :"test 1", "description" : "descrizione test 1"}
            status = status_service.create(valid_status_data)

            invalid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Esiste gia uno stato con questo nome")

    #Test id non presente
    def test_repository_create_status_id_not_existing(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"name" :"test 1", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il campo id non è presente")

    #Test id vuoto
    def test_repository_create_status_id_empty(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "","name" :"test 1", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il campo id non è valido")

    #Test id lungo
    def test_repository_create_status_id_too_long(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-0012", "name" :"test 1", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"L'id deve avere massimo 5 caratteri")

    #Test name non presente
    def test_repository_create_status_name_not_existing(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-001", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il campo name non è presente")

    #Test name vuoto
    def test_repository_create_status_name_empty(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-001","name" :"", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il campo name non è valido")

    #Test name lungo
    def test_repository_create_status_name_too_long(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-001", "name" :"test 1111111111111111111111111111111111111111111111111111111111111", "description" : "descrizione test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il nome deve avere massimo 30 caratteri")

    #Test description non presente
    def test_repository_create_status_description_not_existing(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-001", "name" :"test 1"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il campo description non è presente")

    #Test description vuoto
    def test_repository_create_status_description_empty(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-001","name" :"test 1", "description" : ""}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"Il campo description non è valido")

    #Test description lungo
    def test_repository_create_status_description_too_long(self):

        with self.assertRaises(AppException) as context:

            invalid_status_data = {"id" : "S-001", "name" :"test 1", "description" : "descrizione test 1eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"}
            status_service.create(invalid_status_data)

        self.assertEqual(str(context.exception),"La descrizione deve avere massimo 100 caratteri")

    #Test get by id
    def test_get_by_id(self):

        valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
        status = status_service.create(valid_status_data)

        s = status_service.get_by_id("S-222")
        self.assertEqual(s.id, "S-222")
        self.assertEqual(s.name, "test 1")
        self.assertEqual(s.description, "descrizione test 1")

    #Test get by non existing id
    def test_get_by_non_existing_id(self):

        with self.assertRaises(AppException) as context:

            s = status_service.get_by_id("S-222")

        self.assertEqual(str(context.exception),"Stato non trovato")

    #Test get all no elements
    def test_get_all(self):

        s = status_service.get_all()
        self.assertEqual(len(s),0)

    #Test get all with elements
    def test_get_all_with_elements(self):

        valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
        status_service.create(valid_status_data)
        valid_status_data_2 = {"id" : "S-223","name" :"test 2", "description" : "descrizione test 2"}
        status_service.create(valid_status_data_2)

        s = status_service.get_all()
        self.assertEqual(len(s),2)
        self.assertEqual(s[0].id,"S-222")
        self.assertEqual(s[0].name,"test 1")
        self.assertEqual(s[0].description,"descrizione test 1")
        self.assertEqual(s[1].id,"S-223")
        self.assertEqual(s[1].name,"test 2")
        self.assertEqual(s[1].description,"descrizione test 2")

    #Test add admitted transtition 
    def test_add_admitted_transition(self):

        valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
        status = status_service.create(valid_status_data)
        valid_status_data_2 = {"id" : "S-223","name" :"test 2", "description" : "descrizione test 2"}
        status_1 = status_service.create(valid_status_data_2)

        result = status_service.add_ammitted_transition("S-222","S-223")
    
        self.assertEqual(result,True)

    #Test add admitted transtition first id not existing
    def test_add_admitted_transition_first_id_not_existing(self):

        with self.assertRaises(AppException) as context:

            status_service.add_ammitted_transition("S-200","S-223")

        self.assertEqual(str(context.exception),"Stato di partenza non trovato")

    #Test add admitted transtition second id not existing
    def test_add_admitted_transition_second_id_not_existing(self):

        with self.assertRaises(AppException) as context:
            valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
            status = status_service.create(valid_status_data)
            status_service.add_ammitted_transition("S-222","S-223")

        self.assertEqual(str(context.exception),"Stato di arrivo non trovato")
    
    #Test add admitted transtition second id not existing
    def test_add_admitted_transition_already_existing(self):

        with self.assertRaises(AppException) as context:
            valid_status_data = {"id" : "S-222","name" :"test 1", "description" : "descrizione test 1"}
            status = status_service.create(valid_status_data)
            valid_status_data_2 = {"id" : "S-223","name" :"test 2", "description" : "descrizione test 2"}
            status_1 = status_service.create(valid_status_data_2)

            status_service.add_ammitted_transition("S-222","S-223")
            status_service.add_ammitted_transition("S-222","S-223")

        self.assertEqual(str(context.exception),"Questa transizione gia esiste")
              


if __name__ == '__main__':
    unittest.main()