from zope.interface import implements
from zope.component import getUtility
from zope.app.component.hooks import getSite

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from upc.genwebupc.browser.interfaces import IExtractInfo, IDatos

import sqlalchemy as sql
from collective.lead.interfaces import IDatabase

class datos(object):
    """ datos implements IDatos
    """
    implements(IDatos)

    id_unitat = None
    nom_cat = None
    nom_esp = None
    nom_ing = None
    direccion = None
    telefono = None
    fax = None
    email = None
    web = None
    director = None
    personal = None
    
    def __init__(self, id_unitat, nom_cat, nom_esp, nom_ing, direccion, telefono, fax, email, web, director, personal):
        self.id_unitat = id_unitat
        self.nom_cat = nom_cat
        self.nom_esp = nom_esp
        self.nom_ing = nom_ing
        self.direccion = direccion
        self.telefono = telefono
        self.fax = fax
        self.email = email
        self.web = web
        self.director = director
        self.personal = personal
        
class ExtractInfo(object):
    """ ExtractInfo implements IExtractInfo, 
        tmp =  ExtractInfo()
        IExtractInfo.providedBy(tmp) --> True
    """
        
    implements(IExtractInfo)

    def getDatos(self, netid):
        """Get an IScreening from a screening id
        """
        
        db = getUtility(IDatabase, name='upcnet.database')
        session = db.session
        return session.query(datos).filter_by(id_unitat=netid)[0]