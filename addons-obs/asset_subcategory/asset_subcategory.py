#-*- coding: utf-8 -*-

from openerp.osv import orm, fields


class account_asset_subcategory(orm.Model):

    _name = 'account.asset.subcategory'

    _columns = {
    'name': fields.char('Category name', size=32, required=True),
    'code': fields.integer('Category code', size=8)
}

account_asset_subcategory()

class account_asset_asset_inherit(orm.Model):
    
    _inherit = 'account.asset.asset'
    _columns = {
            'subcategory_id': fields.many2one('account.asset.subcategory', 'Subcategory')
            }
account_asset_asset_inherit()
