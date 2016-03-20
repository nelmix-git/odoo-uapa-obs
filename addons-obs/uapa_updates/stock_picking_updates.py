#-*- coding: utf-8 -*-

from openerp.osv import orm, fields


class StockMove(orm.Model):
    _inherit = 'stock.move'
    _columns = {
        'analytic_id': fields.many2one('account.analytic.account', 'Cost center')
    }

    def _create_account_move_line(self, cr, uid, move,
                                  src_account,
                                  dest_account_id,
                                  reference_amount,
                                  reference_currency_id, context=None):
        """Override function that creates account moves and adds analytic account id.
        For reference, original function found in module stock, line 2420.
        """
        new_account_moves = super(StockMove, self)._create_account_move_line(cr, uid, move,
                                                                         src_account,
                                                                         dest_account_id,
                                                                         reference_amount,
                                                                         reference_currency_id,
                                                                         context)
        #return value is list of tuples for creating a new one2many field
        #[(0, 0, debit_values), (0, 0, credit_values)]
        debit_values = new_account_moves[0][2]
        debit_values['analytic_account_id'] = move.analytic_id.id
        credit_values = new_account_moves[1][2]
        credit_values['analytic_account_id'] = move.analytic_id.id
        return [(0, 0, debit_values), (0, 0, credit_values)]



