import unittest2 as unittest
from upc.genwebupc.testing import GENWEBUPC_INTEGRATION_TESTING
from AccessControl import Unauthorized

class IntegrationTest(unittest.TestCase):

    layer = GENWEBUPC_INTEGRATION_TESTING
    
    def testSetupViewAvailable(self):
        portal = self.layer['portal']
        self.failUnless(portal.unrestrictedTraverse('@@setup-view'))
        
    def testSetupViewNotAvailableForAnonymous(self):
        portal = self.layer['portal']
        self.assertRaises(Unauthorized, portal.restrictedTraverse, '@@setup-view')