##bind context=context
# -*- coding: utf-8 -*-

form = context.REQUEST.form 
session = context.REQUEST.SESSION

if 'wizard' in form.keys():
    if form.get('ajax_load', None): 
        session['ajax_load'] = form.get('ajax_load',None)
    
    if form.get('ajax_include_head', None):
        session['ajax_include_head'] = form.get('ajax_include_head',None)
