from persistent import Persistent

from zope.interface import implements
from zope.component import getUtility

from collective.lead import Database

from sqlalchemy.engine.url import URL
from sqlalchemy import Table
from sqlalchemy.orm import mapper, relation

from upc.genwebupc.extractInfo import datos

class ExtractInformation(Database):
    """The reservations database - registered as a utility providing
    collective.lead.interfaces.IDatabase'
    """

    @property
    def _url(self):
        return URL(drivername='mysql', username='www-estudis',
                   password='bdestudis', host='raiden.upc.es',
                   port=3306, database='www-estudis')
            
    def _setup_tables(self, metadata, tables):
        """Map the database structure to SQLAlchemy Table objects
        """
        tables['upc_unitat'] = Table('upc_unitat', metadata, autoload=True)
    
    def _setup_mappers(self, tables, mappers):
        """Map the database Tables to SQLAlchemy Mapper objects
        """
        mappers['upc_unitat'] = mapper(datos, tables['upc_unitat'])