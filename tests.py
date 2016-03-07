import app as amamb
import unittest

class MainTestCase(unittest.TestCase):

    def setUp(self):
        amamb.app.config['TESTING'] = True
        amamb.debug()
        self.app = amamb.app.test_client()

    def tearDown(self):
    	pass

if __name__ == '__main__':
    unittest.main()
