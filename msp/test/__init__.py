import cell_tests
import schedule_tests

import unittest

def suite():
  loader = unittest.TestLoader()
  suite = unittest.TestSuite()
  suite.addTest(cell_tests.suite())
  suite.addTest(schedule_tests.suite())
  return suite

if __name__ == '__main__':
  unittest.TextTestRunner(verbosity=2).run(suite())
