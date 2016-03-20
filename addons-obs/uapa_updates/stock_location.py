# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:14:14 2013

@author: Carlos Llamacho
"""
from openerp.osv import osv, fields, orm

class stock_location_department(orm.Model):
    """Class that adds a new relation between the hr.department table and
    stock.location one."""

    _name = "stock.location"
    _inherit = "stock.location"
    _columns = {
    'department_id': fields.many2one('hr.department', 'Department')
    }

stock_location_department()
