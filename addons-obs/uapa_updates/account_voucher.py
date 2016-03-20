#-*- coding: utf-8 -*-

from openerp.osv import orm, fields
import number_to_letter
import pdb

class AccountVoucher(orm.Model):

    _inherit = 'account.voucher'
    
    _description = 'Secuencia de Registros'
    _inherit = 'account.voucher'
    
    def _get_journal_sequence(self, cr, uid, ids, name, args, context=None):
        if context is None:
            context = {}
        res = {}
        voucher_obj = self.pool.get('account.voucher')
        for voucher in voucher_obj.browse(cr, uid, ids, context):
            res[voucher.id] = voucher.journal_id.internal_sequence_id.number_next_actual
        return res

    _columns = {
        'name': fields.text('Memoria', required=True),
        'voucher_number': fields.function(_get_journal_sequence, 'Number', readonly=True, digits=(12,0), store=True),
        #'voucher_number': fields.function(_get_journal_sequence, type='char', 'Number', readonly=True, store=False),
        #'voucher_number': fields.char('Number', readonly=True, store=True),
    }
    
    _defaults = {
        #'voucher_number': lambda obj, cr, uid, context: '/',
    }

AccountVoucher()
