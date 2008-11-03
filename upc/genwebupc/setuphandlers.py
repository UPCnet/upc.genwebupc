from Products.CMFCore.utils import getToolByName

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
    
