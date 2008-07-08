from zope.interface import Interface
from zope.component import adapts
from zope.formlib.form import FormFields
from zope.interface import implements
from zope.schema import Bool
from zope.schema import Choice
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot

from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import DropdownChoiceWidget

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from persistent import Persistent

from upc.genwebupc.browser.interfaces import IgenWebControlPanel, IgenWebUtility


class GenWebControlPanelUtility(Persistent):
    """Clase que implementa la utilitat i la fa persistent
    """
    implements(IgenWebUtility)
    especial = False
    columna1 = []
    columna2 = []
    columna3 = []

class GenWebControlPanelAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(IgenWebControlPanel)

    def __init__(self, context):
        super(GenWebControlPanelAdapter, self).__init__(context)
        self.context = getToolByName(context, 'portal_skins')
        self.jstool = getToolByName(context, 'portal_javascripts')
        ptool = getToolByName(context, 'portal_properties')
        self.props = ptool.site_properties

    def get_theme(self):
        return self.context.getDefaultSkin()

    def set_theme(self, value):
        self.context.default_skin = value

    theme = property(get_theme, set_theme)

    @apply
    def especial():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especial
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especial = value
        return property(get, set)
    
    @apply
    def columna1():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.columna1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.columna1 = value
        return property(get, set)

    @apply    
    def columna2():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.columna2
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.columna2 = value
        return property(get, set)

    @apply
    def columna3():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.columna3
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.columna3 = value
        return property(get, set)

class GenWebControlPanel(ControlPanelForm):

    form_fields = FormFields(IgenWebControlPanel)
    form_fields = form_fields.select('theme','especial','columna1','columna2','columna3')
    form_fields['theme'].custom_widget = DropdownChoiceWidget

    label = _("genWeb settings")
    description = _("Settings that configures the behaviour.")
    form_name = _("genWeb settings")
