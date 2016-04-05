#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class AccountJournal(orm.Model):

    _inherit = 'account.journal'
    _columns = {
        'analytic_journal_id': fields.many2one('account.analytic.journal', 'Analytic Journal', required=True),
        'allow_transfer': fields.boolean('Permitir transferencia bancaria')
    }
