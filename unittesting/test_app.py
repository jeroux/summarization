import os
import unittest
import time
from app.app import TEST_VALUE

PATH = os.path.dirname(__file__)
ROOTPATH = os.path.dirname(PATH)


class TestApp(unittest.TestCase):
    def test_variables(self):
        self.assertEqual("Hello World!", TEST_VALUE)

    # def test_streamlit(self):
    #     os.system(f'cd {ROOTPATH}')
    #     os.system("streamlit run app/app.py")
    #     time.sleep(10)
    #     os.system("^C")


if __name__ == "__main__":
    unittest.main()
