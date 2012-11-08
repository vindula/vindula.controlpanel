##bind context=context
# -*- coding: utf-8 -*-

session = context.REQUEST.SESSION
form = context.REQUEST.form 

if not 'wizard' in form.keys():

    if 'ajax_load' in session.keys(): 
        session.delete('ajax_load')
    
    if 'ajax_include_head' in session.keys():
        session.delete('ajax_include_head')

return 'OK'