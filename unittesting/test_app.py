from app.app import TEST_VALUE
import unittest
class TestApp(unittest.TestCase):
    def test_variables(self):
        self.assertEqual("Hello World!", TEST_VALUE)

if __name__ == "__main__":
    unittest.main()