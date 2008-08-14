from zope.interface import Interface, Attribute
from plone.app.controlpanel.skins import ISkinsSchema 
import zope.schema 

from Products.CMFPlone import PloneMessageFactory as _

class IgenWebUtility(Interface):
    """Marker Interface de la utility del control panel del genWeb
    """
class IgenWebControlPanelSchemaGeneral(Interface):

    columna1 = zope.schema.List(__name__='columna1', title=u"Contingut de la columna 1",value_type=zope.schema.Choice(values=['Agenda', 'Noticies', 'Noticies_Actualitat']), default=[])
    columna2 = zope.schema.List(__name__='columna2', title=u"Contingut de la columna 2",value_type=zope.schema.Choice(values=['Agenda_Calendari_petit', 'Actualitat_Noticies_petit']), default=[])
    columna3 = zope.schema.List(__name__='columna3', title=u"Contingut de la columna 3",value_type=zope.schema.Choice(values=['Agenda_mini', 'Actualitat_Noticies_mini','Banners', 'Enquesta']), default=[])
  
    
class IgenWebControlPanelSchemaEspecifics(Interface):
    """ Marker interface de la pestanya dels colors especifics i altres opcions        
    """
    especific1 = zope.schema.TextLine(title=_(u'Color especific 1'),)
    especific2 = zope.schema.TextLine(title=_(u'Color especific 2'),)
    especific3 = zope.schema.TextLine(title=_(u'Color especific 3'),)
    especific4 = zope.schema.TextLine(title=_(u'Color especific 4'),)
    especific5 = zope.schema.TextLine(title=_(u'Color especific 5'),)
    especific6 = zope.schema.TextLine(title=_(u'Color especific 6'),)

class IgenWebControlPanel(IgenWebControlPanelSchemaGeneral, ISkinsSchema, IgenWebControlPanelSchemaEspecifics):
    """ Marker interface de la unio del schema especific de genweb i el dels skins estandar
        de plone i segregat en la pestanya principal
    """  