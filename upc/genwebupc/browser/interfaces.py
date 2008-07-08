from zope.interface import Interface, Attribute
from plone.app.controlpanel.skins import ISkinsSchema 
import zope.schema 

from Products.CMFPlone import PloneMessageFactory as _

class IgenWebUtility(Interface):
    """Marker Interface de la utility del control panel del genWeb
    """
class IgenWebControlPanelSchema(Interface):

    especial = zope.schema.Bool(title=_(u'Mark external links'),
                              description=_(u"If enabled all external links "
                                             "will be marked with link type "
                                             "specific icons. If disabled "
                                             "the 'external links open in new "
                                             "window' setting has no effect."),
                              default=True)
    
    columna1 = zope.schema.List(__name__='columna1', title=u"Contingut de la columna 1",value_type=zope.schema.Choice(values=['Agenda', 'Noticies', 'Noticies i Actualitat']), default=[])
    columna2 = zope.schema.List(__name__='columna2', title=u"Contingut de la columna 2",value_type=zope.schema.Choice(values=['Agenda mini', 'Calendari', 'Noticies i Actualitat mini','Enquesta']), default=[])
    columna3 = zope.schema.List(__name__='columna3', title=u"Contingut de la columna 3",value_type=zope.schema.Choice(values=['Agenda mini', 'Calendari', 'Noticies i Actualitat mini','Enquesta']), default=[])
    
class IgenWebControlPanel(IgenWebControlPanelSchema, ISkinsSchema):
    """ Marker interface de la unio del schema especific de genweb i el dels skins estandar
        de plone
    """