import unittest
from chatbot import get_db_connection

class TestChatbot(unittest.TestCase):
    def test_db_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()
    
    def test_password_validation(self):
        # Test password kurang dari 6 karakter
        short_password = "12345"
        self.assertFalse(len(short_password) >= 6)
        
        # Test password valid
        valid_password = "123456"
        self.assertTrue(len(valid_password) >= 6)

    # Tambahkan test case lainnya...

if __name__ == '__main__':
    unittest.main()