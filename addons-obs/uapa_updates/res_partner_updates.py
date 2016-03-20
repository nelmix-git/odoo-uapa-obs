# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 19:38:58 2013

@author: Carlos Llamacho
"""

from openerp.osv import fields, orm
'''
class res_partner(orm.Model):
    _name="res.partner"
    _inherit="res.partner"

    _columns = {
    'phone': fields.char('Phone', size=64, required=True),
    'email': fields.char('Email', size=240, required=True),
    'child_ids': fields.one2many('res.partner', 'parent_id', 'Contacts', domain=[('active','=',True)], required=True),
    'vat': fields.char('TIN', size=32, help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements.", required=False),
    'credit_limit': fields.float(string='Credit Limit', required=True),
    'street': fields.char('Street', size=128, required=True),
    'street2': fields.char('Street2', size=128, required=True),
    'city': fields.char('City', size=128, required=True),
    'country_id': fields.many2one('res.country', 'Country', required=True),
    }

res_partner()
'''
