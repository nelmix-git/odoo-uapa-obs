# -*- coding: utf-8 -*-
from openerp.osv import orm, fields
from openerp import SUPERUSER_ID

class SubsidiaryCompany(orm.Model):

    _name = 'res.company.subsidiary'
    _inherit = 'res.company'

    def _subsidiary_default_get(self, cr, uid, model=False, field=False, context=None):
        if not context:
            context = {}
        user = self.pool.get('res.users').browse(cr, SUPERUSER_ID, uid, context=context)
        return user.subsidiary_id.id

    def create(self, cr, uid, vals, context=None):
        if not vals.get('name', False) or vals.get('company_id', False):
            self.cache_restart(cr)
            return orm.Model.create(self, cr, uid, vals, context)
        partner = self.pool.get('res.partner')
        partner_id = partner.create(cr, uid, {'name': vals.get('name'),
                                    'is_company': True,
                                    'image': vals.get('logo', False)}, context)
        vals['partner_id'] = partner_id
        subsidiary_id = orm.Model.create(self, cr, uid, vals, context)
        return subsidiary_id

    _columns = {
        'parent_id': fields.many2one('res.company.subsidiary',
                                             'Subsidiaria Padre', select=True)
    }

SubsidiaryCompany()


class Users(orm.Model):

    _inherit = 'res.users'

    def _check_subsidiary(self, cr, uid, ids, context=None):
        """Return allowed subsidiaries for said user.
        Used in constraints."""
        #GLP (Gotta Love Python)
        return all(((this.subsidiary_id in this.subsidiary_ids) or not this.subsidiary_ids) for this in self.browse(cr, uid, ids, context))

    _constraints = [
        (_check_subsidiary, """The chosen subsidiary is not allowed for this user.""", ['subsidiary_id', 'subsidiary_ids'])]


class stock_picking(orm.Model):

    _inherit = 'stock.picking'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'stock.picking', context=c),
    }
stock_picking()

#
class stock_move(orm.Model):

    _inherit = 'stock.move'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'stock.move', context=c),
    }
stock_move()
#
class stock_inventory_line(orm.Model):

    _inherit = 'stock.inventory.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'stock.inventory.line', context=c),
    }
stock_inventory_line()
#
class stock_inventory(orm.Model):

    _inherit = 'stock.inventory'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'stock.inventory', context=c),
    }
stock_inventory()
#
class sale_order_line(orm.Model):

    _inherit = 'sale.order.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'sale.order.line', context=c),
    }
sale_order_line()
#
class sale_order(orm.Model):

    _inherit = 'sale.order'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'sale.order', context=c),
    }
sale_order()
#
class purchase_requisition_line(orm.Model):

    _inherit = 'purchase.requisition.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'purchase.requisition.line', context=c),
    }
purchase_requisition_line()
#
class purchase_requisition(orm.Model):

    _inherit = 'purchase.requisition'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'purchase.requisition', context=c),
    }
purchase_requisition()
#
class purchase_order(orm.Model):

    _inherit = 'purchase.order'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'purchase.order', context=c),
    }
purchase_order()
#
class purchase_order_line(orm.Model):

    _inherit = 'purchase.order.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'purchase.order.line', context=c),
    }
purchase_order_line()
#
class procurement_order(orm.Model):

    _inherit = 'procurement.order'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'procurement.order', context=c),
    }
procurement_order()
#
class crossovered_budget_lines(orm.Model):

    _inherit = 'crossovered.budget.lines'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'crossovered.budget.lines', context=c),
    }
crossovered_budget_lines()
#
class crossovered_budget(orm.Model):

    _inherit = 'crossovered.budget'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'crossovered.budget', context=c),
    }
crossovered_budget()
#
class account_voucher_line(orm.Model):

    _inherit = 'account.voucher.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'account.voucher.line', context=c),
    }
account_voucher_line()
#
class account_voucher(orm.Model):

    _inherit = 'account.voucher'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'account.voucher', context=c),
    }
account_voucher()
#
class account_invoice(orm.Model):

    _inherit = 'account.invoice'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=True),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'account.invoice', context=c),
    }
account_invoice()

class account_invoice(orm.Model):

    _inherit = 'account.journal'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=False, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'account.journal', context=c),
    }
account_invoice()

class hr_employee(orm.Model):

    _inherit = 'hr.employee'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'hr.employee', context=c),
    }
hr_employee()

class account_move(orm.Model):
    _inherit = 'account.move'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'account.move', context=c),
    }

account_voucher()

class account_move_line(orm.Model):
    _inherit = 'account.move.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'account.move.line', context=c),
    }

account_move_line()

class hr_payslip_run(orm.Model):
    _inherit = 'hr.payslip.run'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'hr.payslip.run', context=c),
    }

hr_payslip_run()

class hr_payslip(orm.Model):
    _inherit = 'hr.payslip'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'hr.payslip', context=c),
    }

hr_payslip()

class hr_payslip_line(orm.Model):
    _inherit = 'hr.payslip.line'

    _columns = {
    'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'hr.payslip.line', context=c),
    }

hr_payslip_line()

class bhd_payslip_run_report(orm.Model):
    _inherit = 'bdh.payslip.run.report'

    _columns = {
        'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=True, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'bdh.payslip.run.report', context=c),
    }

bhd_payslip_run_report()

class pos_session(orm.Model):
    _inherit = 'pos.session'

    _columns = {
        'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=False, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'pos.session', context=c),
    }

class pos_order(orm.Model):
    _inherit = 'pos.order'

    _columns = {
        'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=False, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'pos.order', context=c),
    }

class pos_config(orm.Model):
    _inherit = 'pos.config'

    _columns = {
        'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=False, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'pos.config', context=c),
    }

class pos_session_opening(orm.Model):
    _inherit = 'pos.session.opening'

    _columns = {
        'subsidiary_id': fields.many2one('res.company.subsidiary', 'Subsidiaria', required=False, readonly=False),
    }

    _defaults = {
        'subsidiary_id': lambda self,cr,uid,c: self.pool.get('res.company.subsidiary')._subsidiary_default_get(cr, uid, 'pos.session.opening', context=c),
    }

