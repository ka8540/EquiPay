import unittest
from unittest.mock import patch
from src.db.contact import check_contacts_exist

class TestCheckContactsExist(unittest.TestCase):
    @patch('src.db.contact.exec_get_all')
    def test_empty_contacts(self, mock_exec_get_all):
        # Test with no contacts
        contacts = []
        result = check_contacts_exist(contacts)
        mock_exec_get_all.assert_not_called()  # Ensure DB function is not called
        self.assertEqual(result, [])

    @patch('src.db.contact.exec_get_all')
    def test_valid_contacts(self, mock_exec_get_all):
        # Test with valid contacts
        contacts = [
            {'contact': '1234567890'},
            {'contact': '1234567890'},  # Duplicate contact
            {'contact': '0987654321'}
        ]
        expected_result = [
            {'user_id': 1, 'firstname': 'Alice'},
            {'user_id': 2, 'firstname': 'Bob'}
        ]
        mock_exec_get_all.return_value = expected_result
        result = check_contacts_exist(contacts)
        mock_exec_get_all.assert_called_once()  # DB function should be called once
        
        # Extract the actual call arguments
        args, kwargs = mock_exec_get_all.call_args
        query, params = args
        self.assertIn('1234567890', params)
        self.assertIn('0987654321', params)
        self.assertEqual(len(params), 2)
        self.assertEqual(result, expected_result)

    @patch('src.db.contact.exec_get_all')
    def test_invalid_contacts(self, mock_exec_get_all):
        # Test with contacts not in the database
        contacts = [{'contact': '0000000000'}]
        mock_exec_get_all.return_value = []
        result = check_contacts_exist(contacts)
        mock_exec_get_all.assert_called_once()
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
