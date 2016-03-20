#-*- coding: utf-8  -*-

#Author: Carlos Llamacho
#Date: 14-October-2013
#Model of asset move

from openerp.osv import osv, fields, orm

class AssetMove(orm.Model):

    _name = 'account.asset.move'
    _columns = {
    'asset_id': fields.many2one('account.asset.asset', 'Asset',
        required=True),
    'asset_code': fields.related('asset_id', 'code', string='Code',
        readonly=True, type="char"),
    'origin_company': fields.many2one('res.company', 'Origin company',
        readonly=True),
    'origin_department': fields.many2one('hr.department',
        'Origin department', readonly=True),
    'destiny_company': fields.many2one('res.company', 'Destiny company'),
    'destiny_department': fields.many2one('hr.department',
        'Destiny department'),
    'date': fields.date('Date', require=True, help="""Date when the
        movement is executed"""),
    'movement_category': fields.selection((('company_change', 'Company change'),
        ('donation', 'Donation'), ('lent', 'Lent')), 'Movement category',
        required=True, help="""The category to wich the movement belongs."""),
    'status': fields.selection((('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancel', 'Cancel')), 'Status', required=True),
    }
    _defaults = {
    'status': 'draft'
    }

    def action_confirm(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'status': 'confirmed'})
        return True

    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'status': 'cancel'})
        return True

    def onchange_asset(self,cr, uid, ids, asset_id, context=None):
        """On change method for the asset. Gets the department and company of
        origin of the asset."""
        account_asset_obj = self.pool.get('account.asset.asset')
        result = {}
        if asset_id:
            asset_rec = account_asset_obj.browse(cr, uid, asset_id, context)
            self.write(cr, uid, ids, {
                'origin_company': asset_rec.company_id.id,
                'origin_department': asset_rec.department_id.id})
            result['value'] = {'origin_company': asset_rec.company_id.id,
                                'origin_department': asset_rec.department_id.id}
            return True

AssetMove()
