# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Author: Naresh Soni
#    Copyright 2015 Cozy Business Solutions Pvt.Ltd(<http://www.cozybizs.com>)
#    Copyright (C) 2010-Today OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from openerp import api, models, fields
from datetime import datetime
import time
from openerp import tools
from openerp.osv import osv, fields as old_fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    has_bank_name = fields.Boolean(
        string='Add Bank Holder',
        help='It will display bank holder input box while you make payment with this payment method')
    has_cheque_number = fields.Boolean(
        string='Add Cheque number',
        help='It will display Cheque name input box while you make payment with this payment method')
    has_cc_number = fields.Boolean(
        string='Add Credit Card number',
        help='It will display Credit Card number input box while you make payment with this payment method')
    has_ba_number = fields.Boolean(
        string='Add Bank Approval number',
        help='It will display Bank Approval number input box while you make payment with this payment method')
    has_trn_number = fields.Boolean(
        string='Add Transaction number',
        help='It will display Transaction number input box while you make payment with this payment method')

class AccountJournal(models.Model):
    _inherit = 'account.bank.statement.line'

    bank_name = fields.Char('Bank Holder')
    cheque_number = fields.Char('Cheque Number')
    cc_number = fields.Char('Credit Card Number')
    ba_number = fields.Char('Bank Approval Number')
    trn_number = fields.Char('Transaction Number')
    has_bank_name = fields.Boolean(related='journal_id.has_bank_name', 
        string='Add Bank Holder',
        help='It will display bank holder input box while you make payment with this payment method')
    has_cheque_number = fields.Boolean(related='journal_id.has_cheque_number',
        string='Add Cheque number',
        help='It will display Cheque name input box while you make payment with this payment method')
    has_cc_number = fields.Boolean(related='journal_id.has_cc_number',
        string='Add Credit Card number',
        help='It will display Credit Card number input box while you make payment with this payment method')
    has_ba_number =  fields.Boolean(related='journal_id.has_ba_number',
        string='Add Bank Approval number',
        help='It will display Bank Approval number input box while you make payment with this payment method')
    has_trn_number = fields.Boolean(related='journal_id.has_trn_number', 
        string='Add Transaction number',
        help='It will display Transaction number input box while you make payment with this payment method')

class PosOrder(models.Model):
    _inherit = "pos.order"
    
    statement_ids = fields.One2many('account.bank.statement.line', 'pos_statement_id', 'Payments', states={'draft': [('readonly', False)],
                                                                                                          'paid': [('readonly', False)],
                                                                                                          'done': [('readonly', False)],
                                                                                                          'invoiced': [('readonly', False)]}, readonly=True)
     
    @api.model
    def _payment_fields(self, ui_paymentline):
        res_dict = super(PosOrder, self)._payment_fields(ui_paymentline)
        res_dict.update({'bank_name': ui_paymentline.get('bank_name',''),'cheque_number': ui_paymentline.get('cheque_number',''),
        'cc_number': ui_paymentline.get('cc_number',''),'ba_number':ui_paymentline.get('ba_number',''),
        'trn_number': ui_paymentline.get('trn_number','')})
        return res_dict
    
    @api.v7
    def add_payment(self, cr, uid, order_id, data, context=None):
        """Create a new payment for the order"""
        context = dict(context or {})
        statement_line_obj = self.pool.get('account.bank.statement.line')
        property_obj = self.pool.get('ir.property')
        order = self.browse(cr, uid, order_id, context=context)
        date = data.get('payment_date', time.strftime('%Y-%m-%d'))
        if len(date) > 10:
            timestamp = datetime.strptime(date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
            ts = old_fields.datetime.context_timestamp(cr, uid, timestamp, context)
            date = ts.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        args = {
            'amount': data['amount'],
            'date': date,
            'name': order.name + ': ' + (data.get('payment_name', '') or ''),
            'partner_id': order.partner_id and self.pool.get("res.partner")._find_accounting_partner(order.partner_id).id or False,
        }

        journal_id = data.get('journal', False)
        statement_id = data.get('statement_id', False)
        assert journal_id or statement_id, "No statement_id or journal_id passed to the method!"

        journal = self.pool['account.journal'].browse(cr, uid, journal_id, context=context)
        # use the company of the journal and not of the current user
        company_cxt = dict(context, force_company=journal.company_id.id)
        account_def = property_obj.get(cr, uid, 'property_account_receivable', 'res.partner', context=company_cxt)
        args['account_id'] = (order.partner_id and order.partner_id.property_account_receivable \
                             and order.partner_id.property_account_receivable.id) or (account_def and account_def.id) or False

        if not args['account_id']:
            if not args['partner_id']:
                msg = _('There is no receivable account defined to make payment.')
            else:
                msg = _('There is no receivable account defined to make payment for the partner: "%s" (id:%d).') % (order.partner_id.name, order.partner_id.id,)
            raise osv.except_osv(_('Configuration Error!'), msg)

        context.pop('pos_session_id', False)

        for statement in order.session_id.statement_ids:
            if statement.id == statement_id:
                journal_id = statement.journal_id.id
                break
            elif statement.journal_id.id == journal_id:
                statement_id = statement.id
                break

        if not statement_id:
            raise osv.except_osv(_('Error!'), _('You have to open at least one cashbox.'))

        args.update({
            'statement_id': statement_id,
            'pos_statement_id': order_id,
            'journal_id': journal_id,
            'ref': order.session_id.name,
            'bank_name' :data.get('bank_name',''),
            'cheque_number' :data.get('cheque_number',''),
            'cc_number':data.get('cc_number',''),
            'ba_number': data.get('ba_number',''),
            'trn_number': data.get('trn_number',''),
        })

        statement_line_obj.create(cr, uid, args, context=context)
        return statement_id

        
