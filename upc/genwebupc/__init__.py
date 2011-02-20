"""Main product initializer
"""

from zope.i18nmessageid import MessageFactory
from upc.genwebupc import config

from Products.Archetypes import atapi
from Products.CMFCore import utils
from Products.CMFCore.permissions import setDefaultRoles

#Comentado por haber pasado los parches a upc.genweb.patches
#import patches

#importa els parches
# GW4 Comentat parches en standby
#from upc.genweb.patches import patches

GenwebMessageFactory = MessageFactory('upc.genwebupc')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    import content
    
    content_types, constructors, ftis = atapi.process_types(
        atapi.listTypes(config.PROJECTNAME),
        config.PROJECTNAME)

    for atype, constructor in zip(content_types, constructors):
        utils.ContentInit('%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types      = (atype,),
            permission         = config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors = (constructor,),
            ).initialize(context)

