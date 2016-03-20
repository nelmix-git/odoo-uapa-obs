#-*- coding: utf-8 -*-

"""
Created on Tue Jul 25

@author: Carlos Llamacho
"""

from openerp.osv import fields, osv

class AccountInvoiceLine(osv.osv):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    _columns = {
    'account_analytic_id':  fields.many2one('account.analytic.account', 'Analytic Account', required=True),
    }


AccountInvoiceLine()
