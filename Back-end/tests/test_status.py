import unittest
from model.status_model import Status
from model.package_model import Package
from model.account_model import Account
from model.admin_model import Admin
from model.user_model import User
from model.courier_model import Courier





class TestStatus(unittest.TestCase):
    
    def test_create_status(self):
        s = Status(id = "S-001", name = "test 1", description = "descrizione test 1")
        self.assertEqual(s.id, "S-001")
        self.assertEqual(s.name, "test 1")
        self.assertEqual(s.description, "descrizione test 1")


if __name__ == '__main__':
    unittest.main()