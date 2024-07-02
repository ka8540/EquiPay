import unittest
from unittest.mock import patch
from src.utilities.swen_344_db_utils import exec_get_all
from src.db.contact import get_contact  # Adjust the import based on your project structure

class TestContactFunctions(unittest.TestCase):

    @patch('src.db.contact.exec_get_all')  # Adjust the patch target based on your project structure
    def test_get_contact_success(self, mock_exec_get_all):
        mock_exec_get_all.return_value = [
            ('John', '123-456-7890'),
            ('Jane', '098-765-4321')
        ]
        
        result = get_contact()
        expected_result = [
            ('John', '123-456-7890'),
            ('Jane', '098-765-4321')
        ]
        
        self.assertEqual(result, expected_result)
        mock_exec_get_all.assert_called_once_with('''SELECT firstname, contact_number FROM "user";''')

if __name__ == '__main__':
    unittest.main()
