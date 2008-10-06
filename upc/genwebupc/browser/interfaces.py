# -*- coding: UTF-8 -*-
from zope.interface import Interface, Attribute
from plone.app.controlpanel.skins import ISkinsSchema 
import zope.schema 

from Products.CMFPlone import PloneMessageFactory as _

class IgenWebUtility(Interface):
    """Marker Interface de la utility del control panel del genWeb
    """
class IgenWebControlPanelSchemaGeneral(Interface):

    columna1 = zope.schema.List(__name__='columna1', title=u"Contingut de la columna 1",value_type=zope.schema.Choice(values=['Agenda', 'Noticies', 'Noticies_Actualitat']), default=[])
    columna2 = zope.schema.List(__name__='columna2', title=u"Contingut de la columna 2",value_type=zope.schema.Choice(values=['Agenda_Calendari', 'Actualitat_Noticies','Actualitat','Noticies']), default=[])
    columna3 = zope.schema.List(__name__='columna3', title=u"Contingut de la columna 3",value_type=zope.schema.Choice(values=['Agenda', 'Actualitat_Noticies','Banners', 'Enquesta']), default=[])

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


class IgenWebControlPanelSchemaInformacio(Interface):
    """ Marker interface de la pestanya dels literals        
    """
    titolespai_ca = zope.schema.TextLine(title=_(u'Titol de l\'espai - [catala]'),required=False)
    titolespai_es = zope.schema.TextLine(title=_(u'Titol de l\'espai - [castella]'),required=False)
    titolespai_en = zope.schema.TextLine(title=_(u'Titol de l\'espai - [angles]'),required=False)    
    firmaunitat_ca = zope.schema.TextLine(title=_(u'Firma de la unitat - [catala]'),required=False)
    firmaunitat_es = zope.schema.TextLine(title=_(u'Firma de la unitat - [castella]'),required=False)
    firmaunitat_en = zope.schema.TextLine(title=_(u'Firma de la unitat - [angles]'),required=False)
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

# Entities found in the database

class IDatos(Interface):
    """ Interface que será implementada por la clase python donde se mapearán las columnas de la tabla sql
    """
    
class IExtractInfo(Interface):
    """ Realiza los querys
    """    

    def getDatos(netid):
        """ Retorna datos de acuerdo a un id
        """

class IFormulario(Interface):
    """Define the fields of our form
    """
    
    nombre = zope.schema.TextLine(title=_(u'Nom'),
                                        description=_(u'Inseriu el vostre nom complet'),
                                        required=True)
                              
    destinatario = zope.schema.TextLine(title=_(u'A/e'),
                                        description=_(u'Si us plau escriviu, la vostra adreça de correu  electrònic'),
                                        required=True)
 
    asunto = zope.schema.TextLine(title=_(u'Assumpte'),
                                        description=_(u'Si us plau, entreu l\'assumpte del missatge que voleu enviar'),
                                        required=True)

    mensaje = zope.schema.TextLine(title=_(u'Missatge'),
                                        description=_(u'Si us plau, escriviu el missatge que voleu enviar'),
                                        required=True)