from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter, getUtility
from upc.genwebupc.browser.interfaces import IgenWebUtility

class HomePageView(BrowserView):
    __call__=ViewPageTemplateFile('homepage.pt')

    def getColumn1(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna1
        
    def getColumn2(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna2
                
    def getColumn3(self):
        """Funcio que agafa els valors de quines caixetes cal posar la
           home page del genweb
        """
        gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
        return gw_util.columna3