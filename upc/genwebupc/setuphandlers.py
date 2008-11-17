from Products.CMFCore.utils import getToolByName
from Products.PloneLDAP.factory import manage_addPloneLDAPMultiPlugin
from Products.LDAPUserFolder.LDAPUserFolder import LDAPUserFolder
from Products.CMFPlone.utils import _createObjectByType

from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from plone.app.controlpanel.mail import IMailSchema

from zope.component import getAdapters



def setupVarious(context):
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('upc.genwebupc_various.txt') is None:
        return
        
    # Add additional setup code here
    # 
    transforms = getToolByName(context, 'portal_transforms')
    transform = getattr(transforms, 'safe_html')
    valid = transform.get_parameter_value('valid_tags')
    nasty = transform.get_parameter_value('nasty_tags')
    valid['embed']=1
    valid['object']=1
    if 'embed' in nasty:
        del nasty['embed']
    if 'object' in nasty:
        del nasty['object']
    kwargs = {}
    kwargs['valid_tags']=valid
    kwargs['nasty_tags']=nasty
    for k in list(kwargs):
        if isinstance(kwargs[k], dict):
            v = kwargs[k]
            kwargs[k+'_key'] = v.keys()
            kwargs[k+'_value'] = [str(s) for s in v.values()]
            del kwargs[k]
    transform.set_parameters(**kwargs)
    transform._p_changed = True
    transform.reload()
    portal = context.getSite()
    try:
            manage_addPloneLDAPMultiPlugin(portal.acl_users, "ldapUPC",
                title="ldapUPC", use_ssl=1, login_attr="cn", uid_attr="cn", local_groups=0,
                users_base="ou=Users,dc=upc,dc=edu", users_scope=2,
                roles="Anonymous", groups_base="ou=Groups,dc=upc,dc=edu",
                groups_scope=2, read_only=True, binduid="cn=ldap.upc,ou=Users,dc=upc,dc=edu", bindpwd="secret",
                rdn_attr="cn", LDAP_server="leia.upc.es", encryption="SSHA")
            portal.acl_users.ldapUPC.acl_users.manage_edit("ldapUPC", "cn", "cn", "ou=Users,dc=upc,dc=edu", 2, "Anonymous", 
                "ou=Groups,dc=upc,dc=edu", 2, "cn=ldap.upc,ou=Users,dc=upc,dc=edu", "secret", 1, "cn",
                "top,person", 0, 0, "SSHA", 1, '')
            plugin = portal.acl_users['ldapUPC']
            plugin.manage_activateInterfaces(['IGroupEnumerationPlugin','IGroupsPlugin','IPropertiesPlugin','IGroupIntrospection','IAuthenticationPlugin','IRolesPlugin','IUserEnumerationPlugin','IRoleEnumerationPlugin'])
            LDAPUserFolder.manage_addServer(portal.acl_users.ldapUPC.acl_users, "han.upc.es", '636', use_ssl=1)
    except: 
            pass


    portal_role_manager = portal.acl_users['portal_role_manager']
    portal_role_manager.assignRolesToPrincipal(["Manager"],"UPC.Plone.Admins")
    portal_role_manager.assignRolesToPrincipal(["Manager"],"UPCnet.Plone.Admins")

    # configurem mail


    mail = IMailSchema(portal) 
    mail.smtp_host = u'relay.upc.es'
    mail.email_from_name = "Administrador del Genweb"
    mail.email_from_address = "noreply@upc.edu"


    
    # Crear carpetes i coleccions, linkades per language, el primer language de la tupla es el canonical
    
    
    news = crearObjecte(portal,'news','Large Plone Folder','News','Site News')
    noticias = crearObjecte(portal,'noticias','Large Plone Folder','Notícias','Notícias del sitio')
    noticies = crearObjecte(portal,'noticies','Large Plone Folder','Notícies','Notícies del lloc')        
    setLanguageAndLink([(noticies,'ca'),(noticias,'es'),(news,'en')])
        
    addCollection(news,'aggregator','News','Site News','News Item','published')
    addCollection(noticias,'aggregator','Notícias','Notícias del sitio','News Item','published')
    addCollection(noticies,'aggregator','Notícies','Notícies del lloc','News Item','published')        
    setLanguageAndLink([(noticies.aggregator,'ca'),(noticias.aggregator,'es'),(news.aggregator,'en')])    
    
    events = crearObjecte(portal,'events','Large Plone Folder','Events','Site Events')
    eventos = crearObjecte(portal,'eventos','Large Plone Folder','Eventos','Eventos del sitio')
    esdeveniments = crearObjecte(portal,'esdeveniments','Large Plone Folder','Esdeveniments','Esdeveniments del lloc')  
    setLanguageAndLink([(esdeveniments,'ca'),(eventos,'es'),(events,'en')])
    
    addCollection(events,'aggregator','Events','Site Events','Event','published')
    addCollection(eventos,'aggregator','Eventos','Eventos del sitio','Event','published')
    addCollection(esdeveniments,'aggregator','Esdeveniments','Esdeveniments del lloc','Event','published')            
    setLanguageAndLink([(esdeveniments.aggregator,'ca'),(eventos.aggregator,'es'),(events.aggregator,'en')])    
    
    banners_en = crearObjecte(portal,'banners-en','BannerContainer','Banners','English Banners')
    banners_es = crearObjecte(portal,'banners-es','BannerContainer','Banners','Banners en Español')
    banners_ca = crearObjecte(portal,'banners-ca','BannerContainer','Banners','Banners en Català')    
    setLanguageAndLink([(banners_ca,'ca'),(banners_es,'es'),(banners_en,'en')])    
    
    logosfooter_en = crearObjecte(portal,'logosfooter-en','Logos_Container','Footer Logos','English footer logos')
    logosfooter_es = crearObjecte(portal,'logosfooter-es','Logos_Container','Logos pie','Logos en español del pie de página')
    logosfooter_ca = crearObjecte(portal,'logosfooter-ca','Logos_Container','Logos peu','Logos en català del peu de página')    
    setLanguageAndLink([(logosfooter_ca,'ca'),(logosfooter_es,'es'),(logosfooter_en,'en')])
            
    #configurar pagines de benvinguda        
            
    setLanguageAndLink([(portal.benvingut,'ca'),(portal.bienvenido,'es'),(portal.welcome,'en')])        
    doWorkflowAction(portal.benvingut,'publish','published')
    doWorkflowAction(portal.bienvenido,'publish','published')    
    doWorkflowAction(portal.welcome,'publish','published')                
    
    
def setLanguageAndLink(items):
    canonical = items[0][0]
    for item,language in items:
        item.setLanguage(language)
        if item!=canonical:
            item.addTranslationReference(canonical)

def doWorkflowAction(context,action,status):
    pw = getToolByName(context, "portal_workflow") 
    object_workflow = pw.getWorkflowsFor(context)[0].id
    object_status = pw.getStatusOf(object_workflow,context)
    if object_status:
        if object_status['review_state']!=status:
            pw.doActionFor(context,action)

    
def crearObjecte(context,id,type_name,title,description,exclude=True,status='published',action='publish'):
    pt = getToolByName(context,'portal_types')
    if not getattr(context,id,False) and type_name in pt.listTypeTitles().keys():
        #creem l'objecte i el publiquem
        _createObjectByType(type_name, context, id)
    #populem l'objecte
    created = context[id]            
    doWorkflowAction(created,action,status)    
    created.setTitle(title)
    created.setDescription(description)

    created.setExcludeFromNav(exclude)
    created.reindexObject()
    return created
    
def addCollection(context,id,title,description,type_filter,state_filter):

    topic = crearObjecte(context,id,'Topic',title,description,False)
    
    # Activem el limit i el posem a 10 notícies
    topic.setLimitNumber(True)
    topic.setItemCount(10)
    
    #Ara afegim els criteris, si no hi son
    criteris = [('Type','ATPortalTypeCriterion'),
        ('review_state','ATSelectionCriterion'),
        ('path','ATPathCriterion'),
        ('modified','ATSortCriterion')]
    for crit in criteris:
        if not getattr(topic,'crit__%s_%s' % (crit[0],crit[1]),False):
            topic.addCriterion(crit[0],crit[1])    

    # Criteri tipus
    criteri_tipus = topic['crit__Type_ATPortalTypeCriterion']
    criteri_tipus.setValue((type_filter))
    criteri_tipus.setOperator('and')

    # criteri estat

    criteri_estat = topic['crit__review_state_ATSelectionCriterion']
    criteri_estat.setValue((state_filter))
    criteri_estat.setOperator('and')

    # criteri ruta = carpeta pare

    criteri_ruta =  topic['crit__path_ATPathCriterion']
    criteri_ruta.setValue([context])
    criteri_ruta.setRecurse(True)


    # Criteri d'ordenació

    criteri_ordenacio = topic['crit__modified_ATSortCriterion']
    criteri_ordenacio.setReversed(True)

    # Posar la vista per defecte de la pàgina principal a la collection que acavem de crear

    context.setDefaultPage(id)
