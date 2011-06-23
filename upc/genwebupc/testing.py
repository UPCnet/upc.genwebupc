from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig

class GenwebUPC(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import upc.genwebupc
        xmlconfig.file('configure.zcml',
                       upc.genwebupc,
                       context=configurationContext)
        
        import Products.PloneLDAP
        xmlconfig.file('configure.zcml',
                       Products.PloneLDAP,
                       context=configurationContext)
        
    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'upc.genwebupc:default')


GENWEBUPC_FIXTURE = GenwebUPC()
GENWEBUPC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(GENWEBUPC_FIXTURE,),
    name="GenwebUPC:Integration")
GENWEBUPC_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(GENWEBUPC_FIXTURE,),
    name="GenwebUPC:Functional")
