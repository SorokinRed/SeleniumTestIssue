import unittest

import GoogleAccountTests

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(GoogleAccountTests.Account)
    unittest.TextTestRunner(verbosity=2).run(suite)