import unittest
from unittest.mock import patch
from src.db.contact import check_contacts_exist, normalize_contact

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
        # Test with valid contacts, including normalization
        contacts = [
            {'contact': '+1234567890'},
            {'contact': '1234567890'},  # Duplicate contact, should be normalized
            {'contact': '+0987654321'}
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
        # Check the normalization and uniqueness are handled correctly
        self.assertIn('+1234567890', params)
        self.assertIn('+0987654321', params)
        self.assertEqual(len(params), 2)  # Ensure duplicate is handled
        self.assertEqual(result, expected_result)

    @patch('src.db.contact.exec_get_all')
    def test_invalid_contacts(self, mock_exec_get_all):
        # Test with contacts not in the database
        contacts = [{'contact': '0000000000'}]  # This should be normalized
        mock_exec_get_all.return_value = []
        result = check_contacts_exist(contacts)
        mock_exec_get_all.assert_called_once()
        
        args, kwargs = mock_exec_get_all.call_args
        query, params = args
        # Ensure normalization is applied even to invalid contacts
        self.assertIn('+0000000000', params)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
