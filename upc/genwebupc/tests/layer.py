from Products.PloneTestCase import ptc

from Products.PloneTestCase.layer import onsetup

from Products.Five import zcml

import collective.testcaselayer.ptc

import upc.genwebupc

@onsetup
def setup_product():
    zcml.load_config('configure.zcml', upc.genwebupc)

setup_product()
ptc.setupPloneSite(products=['upc.genwebupc'])

class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):
        # Install the upc.genwebupc product
        self.addProfile('upc.genwebupc:default')

Layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])