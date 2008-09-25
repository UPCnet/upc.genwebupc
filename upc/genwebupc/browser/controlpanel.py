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

from plone.fieldsets.fieldsets import FormFieldsets

from persistent import Persistent

from upc.genwebupc.browser.interfaces import *
from plone.app.controlpanel.skins import ISkinsSchema 

class GenWebControlPanelUtility(Persistent):
    """Clase que implementa la utilitat i la fa persistent
    """
    implements(IgenWebUtility)
    
    # de la pestanya general
    columna1 = []
    columna2 = []
    columna3 = []

    # de la pestanya d'especifics
    especific1=''
    especific2=''
    especific3=''
    especific4=''
    especific5=''
    especific6=''

    imatgedefonsprops=''

    barraidiomesbool = False
    
    # de la pestanya d'informació
    titolespai_ca = ''
    titolespai_en =''
    titolespai_es = ''
    firmaunitat_ca = ''
    firmaunitat_en = ''
    firmaunitat_es = ''
    enllaslogotip = ''
    contacteid = ''
    contactegmaps = ''
    
    # de la pestanya de sabors
    tipusintranet = ''
    titolcapsaleraMaster = ''
    idestudiMaster = ''
    idtitulacioMaster = ''

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

    @apply
    def especific1():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)

    @apply
    def especific2():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)

    @apply
    def especific3():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)

    @apply
    def especific4():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)

    @apply
    def especific5():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)            

    @apply
    def especific6():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.especific1
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.especific1 = value
        return property(get, set)

    @apply
    def imatgedefonsprops():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.imatgedefonsprops
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.imatgedefonsprops = value
        return property(get, set)

    @apply
    def barraidiomesbool():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.barraidiomesbool
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.barraidiomesbool = value
        return property(get, set)

    @apply
    def titolespai_ca():
        def get(self):
            import pdb;pdb.set_trace()
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolespai_ca
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolespai_ca = value
        return property(get, set)

    @apply
    def titolespai_en():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolespai_en
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolespai_en = value
        return property(get, set)

    @apply
    def titolespai_es():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolespai_es
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolespai_es = value
        return property(get, set)
            
    @apply
    def firmaunitat_ca():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.firmaunitat_ca
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_ca = value
        return property(get, set)

    @apply
    def firmaunitat_en():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.firmaunitat_en
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_en = value
        return property(get, set)

    @apply
    def firmaunitat_es():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.firmaunitat_es
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.firmaunitat_es = value
        return property(get, set)

    @apply
    def enllaslogotip():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.enllaslogotip
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.enllaslogotip = value
        return property(get, set)

    @apply
    def contacteid():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.contacteid
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.contacteid = value
        return property(get, set)

    @apply
    def contactegmaps():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.contactegmaps
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.contactegmaps = value
        return property(get, set)

    @apply
    def tipusintranet():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.tipusintranet
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.tipusintranet = value
        return property(get, set)

    @apply
    def titolcapsaleraMaster():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.titolcapsaleraMaster
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.titolcapsaleraMaster = value
        return property(get, set)

    @apply
    def idestudiMaster():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.idestudiMaster
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.idestudiMaster = value
        return property(get, set)

    @apply
    def idtitulacioMaster():
        def get(self):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            return gw_util.idtitulacioMaster
        def set(self, value):
            gw_util = getUtility(IgenWebUtility, "GenWebControlPanelUtility")
            gw_util.idtitulacioMaster = value
        return property(get, set)
                                        
    
    
general = FormFieldsets(ISkinsSchema['theme'], IgenWebControlPanelSchemaGeneral)
general.id = 'genWebControlPanelgeneral'
general.label = _(u'label_gwcp_general', default=u'General')
general['theme'].custom_widget = DropdownChoiceWidget

especifics = FormFieldsets(IgenWebControlPanelSchemaEspecifics)
especifics.id = 'genWebControlPanelespecifics'
especifics.label = _(u'label_gwcp_especifics', default=u'Especific')

informacio = FormFieldsets(IgenWebControlPanelSchemaInformacio)
informacio.id = 'genWebControlPanelinformacio'
informacio.label = _(u'label_gwcp_informacio', default=u'Informacio')

sabors = FormFieldsets(IgenWebControlPanelSchemaSabors)
sabors.id = 'genWebControlPanelsabors'
sabors.label = _(u'label_gwcp_sabors', default=u'Sabors')
sabors['tipusintranet'].custom_widget = DropdownChoiceWidget

class GenWebControlPanel(ControlPanelForm):

    form_fields = FormFieldsets(general, informacio, especifics, sabors)

    #form_fields = form_fields.select('theme','especial','columna1','columna2','columna3')
    #form_fields.fieldsets[0] = form_fields.fieldsets[0].select('theme','especial','columna1','columna2','columna3')

    label = _("genWeb settings")
    description = _("Settings that configures the behaviour of the genWeb.")
    form_name = _("genWeb settings")
