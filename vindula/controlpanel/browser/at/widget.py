# -*- coding: utf-8 -*-
import types
from zope.component import ComponentLookupError
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

from zope.app.component.hooks import getSite
from Products.PythonScripts.standard import url_quote

from Products.Archetypes.config import REFERENCE_CATALOG
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

from five import grok
from zope.interface import Interface

class VindulaReferenceSelectionWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "referencebrowserpopup",
        'helper_js': ('referencebrowserpopup.js',),                                

        'size'                  : 40,
        'popup_width'           :900,
        'popup_height'          :500,
        'allowupload'           : True,
        'allowaddfolder'        : True,
        'typeview'              :'image',
        
        'allow_sorting'         : False,
        'review_state'          : '',
        
        'image_portal_types'    :('Image'),
        'image_method'          :'image_thumb',
        'show_path'             :False,
        
        })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """Basic impl for form processing in a widget
        """
        result = super(VindulaReferenceSelectionWidget,
                       self).process_form(instance, field, form, empty_marker,
                                          emptyReturnsMarker, validating)
        # when removing all items from a required reference-field we get a
        # default form value of [''].  here we inject a 'custom' empty-value
        # to trigger the isempty-validator and not use the previous content of
        # the field.
        if field.required and field.multiValued and \
           not emptyReturnsMarker and result == ([''], {}):
            return [], {}

        return result
    
    security.declarePublic('getUrlFinder')
    def getUrlFinder(self,field):
        url_finder = 'refbrowser_finder?fieldName=%s&mult=%s&' %(field.getName(),field.multiValued)
        url_finder += 'typeview=%s&media=%s&allowimagesizeselection:boolean=False&' %(self.typeview,self.typeview)
        if self.allowupload:
            url_finder += 'allowupload:boolean=%s&' %self.allowupload
        if self.allowaddfolder:
            url_finder += 'allowaddfolder:boolean=%s&' %self.allowaddfolder
            
        if field.allowed_types:
            if type(field.allowed_types) == tuple:   
                for itype in tuple(field.allowed_types):
                    url_finder += 'types:list=%s&' % url_quote(itype)
            else:
                url_finder += 'types:list=%s&' % url_quote(field.allowed_types)
        
        if self.review_state:
            url_finder += 'review_state=%s&' %url_quote(self.review_state)
        
        return url_finder

registerWidget(
    VindulaReferenceSelectionWidget,
    title='Reference and Add File Widget',
    description=('You can select or add files from a popup window.'),
    used_for=('Products.Archetypes.Field.ReferenceField'))


class AjaxLoadContentReferenceView(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('vindula-reference-ajax')

    def render(self):
        form = self.request.form
        fieldName = form.get('nameField','')
        html = ''
        html += '<div id="ref_browser_%s_content_edit">'%(fieldName)
        try:
            if self.obj.portal_type in ('Image'):
                html += '<img src=%s />' %(self.obj.absolute_url() + '/image_thumb')
                html += '<br />'
        except:
            pass
        
        html += '</div>'
        
        return html
    
    def update(self):
        form = self.request.form
        if 'uid' in form.keys():
            uid = form.get('uid','')
            catalog = getToolByName(aq_inner(self.context), REFERENCE_CATALOG)
            self.obj = catalog.lookupObject(uid)
            
        else:
            self.obj = ''
