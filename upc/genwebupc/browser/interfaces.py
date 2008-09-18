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
    
    imatgedefonsprops = zope.schema.TextLine(title=_(u'Tipus de repeat de la imatge de fons (?)'),required=False)

    barraidiomesbool = zope.schema.Bool(title=_(u'Mostrar barra de idiomes?'),required=False)

class IgenWebControlPanelSchemaInformacio(Interface):
    """ Marker interface de la pestanya dels literals        
    """
    titolespai_ca = zope.schema.TextLine(title=_(u'Titol de l\'espai &nbsp;&nbsp;-&nbsp;&nbsp; [catala]'),required=False)
    titolespai_es = zope.schema.TextLine(title=_(u'Titol de l\'espai &nbsp;&nbsp;-&nbsp;&nbsp; [castella]'),required=False)
    titolespai_en = zope.schema.TextLine(title=_(u'Titol de l\'espai &nbsp;&nbsp;-&nbsp;&nbsp; [angles]'),required=False)    
    firmaunitat_ca = zope.schema.TextLine(title=_(u'Firma de la unitat &nbsp;&nbsp;-&nbsp;&nbsp; [catala]'),required=False)
    firmaunitat_es = zope.schema.TextLine(title=_(u'Firma de la unitat &nbsp;&nbsp;-&nbsp;&nbsp; [castella]'),required=False)
    firmaunitat_en = zope.schema.TextLine(title=_(u'Firma de la unitat &nbsp;&nbsp;-&nbsp;&nbsp; [angles]'),required=False)
    enllaslogotip = zope.schema.TextLine(title=_(u'Enllac logotip de la unitat'),required=False)
    contacteid = zope.schema.TextLine(title=_(u'ID de la BBDD de UBs'),required=False)
    contactegmaps = zope.schema.TextLine(title=_(u'Codi URL google maps'),required=False)
    
class IgenWebControlPanelSchemaSabors(Interface):
    """ Marker interface de la pestanya de la informació sobre els sabors        
    """
    tipusintranet = zope.schema.Choice(title=_(u'Tipus de intranet'), values=['Visible', 'Discreta'], required=False)
    titolcapsaleraMaster = zope.schema.TextLine(title=_(u'Titol de capsalera del master'),required=False)
    idestudiMaster = zope.schema.TextLine(title=_(u'id_estudi'),required=False)
    idtitulacioMaster = zope.schema.TextLine(title=_(u'id_titulacio'),required=False)
    
class IgenWebControlPanel(IgenWebControlPanelSchemaGeneral, ISkinsSchema, IgenWebControlPanelSchemaEspecifics, IgenWebControlPanelSchemaInformacio, IgenWebControlPanelSchemaSabors):
    """ Marker interface de la unio del schema especific de genweb i el dels skins estandar
        de plone i segregat en la pestanya principal
    """  