#-*- coding: utf-8 -*-

from openerp.osv import orm, fields


class AccountJournal(orm.Model):

    _inherit = 'account.journal'

    _columns = {
    'is_salary_journal': fields.boolean('Salary Journal', help="""Mark this
        field if this diary is related to the employees salary."""),
    'is_credit_card': fields.boolean('Credit card', help="""Mark this field
        if this diary is related to credits cards."""),
    'porcentual_value': fields.float('Porcental value', help="""For percent
        enter a ratio between 0-1."""),
    'expense_account': fields.many2one('account.account', 'Expense account',
        domain="[('type','=','other')]")
    }

AccountJournal()
