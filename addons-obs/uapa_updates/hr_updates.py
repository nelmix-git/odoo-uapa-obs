# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 20:51:14 2013

@author: Carlos Llamacho
"""

import logging
import time
from datetime import datetime
from dateutil import relativedelta
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import pdb

class hr_employee(orm.Model):
    _name='hr.employee'
    _inherit='hr.employee'

    _columns = {
        'partner_phone':fields.char('Telefono Personal', size=32),
        'emergency_contact':fields.one2many('hr.employee.emergency.contact', 'employee_id', 'Contactos de Emergencia'),
        'family_info_ids':fields.one2many('hr.employee.family', 'employee_id', 'Informacion Familiar'),
        'nss_id':fields.char('NSS', size=32),
        'hr_employee_ars_id':fields.many2one('hr.employee.ars', 'ARS Afiliado', required=False),
        'employee_code':fields.char('Code', size=32, required=True, readonly=True),
        'events_ids_registration':fields.one2many('event.registration', 'employee_id', 'Registro de Evento de Entrenamiento'),
        #'event_training_id':fields.related('events_ids_registration', 'event_id', 'registration_ids', relation='event.event',  type='one2many', string='Event',  domain="[('is_training','=',True)]")
        'formation_ids': fields.one2many('hr.employee.formation', 'employee_id', 'Formacion', ondelete="cascade"),
    }

    _defaults = {
    'employee_code':lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'employee.number')
    }

    def create(self, cr, uid, ids, context=None):
        """Overwritten to the create method of employee so that it creates a res_partner record as well."""

        partner_obj = self.pool.get('res.partner')
        values = ids
        created_id = super(hr_employee, self).create(cr, uid, values, context)
        created_partner_id = partner_obj.create(cr, uid, {'name': values.get('name'),
                                     'display_name': values.get('name_related'),
                                     'lang': 'es_DO',
                                     'active': True,
                                     'email': values.get('work_email'),
                                     'phone': values.get('work_phone'),
                                     'employee': True,
                                     'tz': 'America/Santo_Domingo',
                                     'notification_email_send': 'comment',
                                     'company_id': values.get('company_id')}, context)
        self.write(cr, uid, created_id, {'address_home_id': created_partner_id}, context)
        return created_id

hr_employee()

class hr_employee_family(orm.Model):
    _name="hr.employee.family"

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Informacion Familiar'),
        'name': fields.char("Name", size=64, required=True),
        'relationship': fields.selection((('father', 'Padre'), ('mother', 'Madre'), ('daughter/son', 'Hijo/Hija'), ('other', 'Otro')), 'Parentezco'),
        'date_of_birth': fields.date('Fecha de Nacimiento', required=True, select=True),
        'gender': fields.selection((('male', 'Masculino'), ('female', 'Femenino')), 'Genero')
    }

hr_employee_family()

class hr_contract(orm.Model):
    _name='hr.contract'
    _inherit='hr.contract'

    '''
    def _current_rate(self, cr, uid, ids, name, arg, context=None):

        if context is None:
            context = {}
        res = {}
        if 'date' in context:
            date = context['date']
        else:
            date = time.strftime('%Y-%m-%d')
            date = date or time.strftime('%Y-%m-%d')

        for id in ids:
            cr.execute("SELECT contract_id, rate FROM hr_contract_rate WHERE contract_id = %s AND name <= %s AND rate <> 0 ORDER BY name desc LIMIT 1" ,(id, date))
            if cr.rowcount:
                id, rate = cr.fetchall()[0]
                res[id] = rate
            else:
                res[id] = 0
        return res
    '''

    def _get_contract_years(self, cr, uid, ids, name, arg, context=None):

        res = {}

        for contract in self.browse(cr, uid, ids, context=context):
            today = datetime.today()
            dt = datetime.strptime(contract.date_start, '%Y-%m-%d')
            dt1 = today - dt
            dt2 = dt1.days
            res[contract.id] = (dt2/365)
        return res

    def _get_contract_days(self, cr, uid, ids, name, arg, context=None):

        res = {}
        for contract in self.browse(cr, uid, ids, context=context):
            today = datetime.today()
            dt = datetime.strptime(contract.date_start, '%Y-%m-%d')
            dt1 = today - dt
            dt2 = dt1.days
            res[contract.id] = dt2
        return res

    _columns = {
        'schedule_pay': fields.selection([
            ('fortnightly', 'Quincenal'),
            ('monthly', 'Mensual'),
            ('quarterly', 'Trimestral'),
            ('semi-annually', 'Semestral'),
            ('annually', 'Anual'),
            ('weekly', 'Semanal'),
            ('bi-weekly', 'Bi-semanal'),
            ('bi-monthly', 'Bi-mensual'),
            ], 'Scheduled Pay', select=True),
        'company_id': fields.many2one('res.company', 'Compañia', required=True),
        'contract_years': fields.function(_get_contract_years, store=True, type='integer', digits_compute=dp.get_precision('Payroll'), string='Years at Work'),
        'contract_days': fields.function(_get_contract_days, store=True, type='integer', digits_compute=dp.get_precision('Payroll'), string='Days at Work'),

    }

    _defaults = {
        'schedule_pay': 'fortnightly',
    }

    def onchange_employee(self, cr, uid, ids, employee, context):

        employee_obj = self.pool.get('hr.employee')
        res = {}
        for contract in self.browse(cr, uid, ids, context):
            employee = employee_obj.browse(cr, uid, employee, context)
            res['value'] = {'job_id': employee.job_id.id,
                            'company_id': employee.company_id.id}
        return res


class hr_recruitment_career(orm.Model):
    _name='hr.recruitment.career'

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'sequence': fields.integer('Sequence', size=2, required=True),
        }

hr_recruitment_career()

class hr_employee_emergency_contact(orm.Model):
    _name='hr.employee.emergency.contact'

    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee', readonly=True),
        'name': fields.char('Name', size=64, required=True),
        'emergency_contact_phone': fields.char('Phone', size=32)
    }

hr_employee_emergency_contact()

# class hr_contract_news(orm.Model):
#     _name='hr.contract.news'
#
#     _columns = {
#         'contract_id': fields.many2one('hr.contract', 'Contrato', required=True),
#         'hr_contract_news_concepts_id': fields.many2one('hr.contract.news.concepts', 'Concepto Novedades Contrato', required=True),
#         'amount': fields.float('Monto', digits_compute=dp.get_precision('Account')),
#         'frecuency_type': fields.selection((('fixed', 'Fijo'),
#                                             ('variable', 'Variable')), 'Tipo de Frecuencia', required=True),
#         'apply_on': fields.selection((('1', 'Primera Quincena'),
#                                       ('2', 'Segunda Quincena'),
#                                       ('3', 'Fin de Mes')), 'Apply On', required=True),
#         'frecuency_number': fields.integer('Numero de Veces'),
#         'start_date': fields.date('Fecha Inicial'),
#         'end_date': fields.date('Fecha Final'),
#     }
#
#     _defaults = {
#         'frecuency_type': 'fixed'
#     }
#
# hr_contract_news()
#
# class hr_contract_news_concepts(orm.Model):
#     _name='hr.contract.news.concepts'
#
#     _columns = {
#         'code': fields.char('Codigo', size=8, required=True),
#         'name': fields.char('Nombre', size=64, required=True),
#         'category_id': fields.many2one('hr.salary.rule.category', 'Categoria', required=True),
#     }
#
# hr_contract_news_concepts()

class hr_employee_ars(orm.Model):
    _name='hr.employee.ars'

    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'sequence': fields.integer('Sequence', size=3, required=True)
    }

hr_employee_ars()

class hr_expense_expense(orm.Model):
    _name='hr.expense.expense'
    _inherit='hr.expense.expense'

    _columns = {
        'expense_type': fields.selection((('general', 'General'), ('event', 'Event'), ('project', 'Project')), 'Type of Event'),
        'event_id': fields.many2one('event.event', 'Event'),
        'proyect_id': fields.many2one('event.event', 'Proyect')
    }
hr_expense_expense()

class hr_payslip(orm.Model):


    _name = 'hr.payslip'
    _inherit = 'hr.payslip'

    _columns = {
        'payment_period': fields.selection((('1', 'Primera Quincena'),
                                            ('2', 'Segunda Quincena'),
                                            ('3', 'Fin de mes')), 'Periodo de Pago', required=True),
        'payroll_type': fields.selection([('administrative', 'Administrativa - UAPA'),
                                          ('educational', 'Docente - UAPA'),
                                          ('administrative_ceges_stgo', 'Administrativa - CEGES Santiago'),
                                          ('educational_ceges_stgo', 'Docente - CEGES Santiago'),
                                          ('administrative_ceges_stdo', 'Administrativa - CEGES Santo Domingo'),
                                          ('educational_ceges_stdo', 'Docente - CEGES Santo Domingo'),
                                          ('vacations', 'Vacaciones'),
                                          ('overtime', 'Horas Extras'),
                                          ('xmas_bonus', 'Salario de Navidad')], 'Tipo de Nomina', required=True),
        'clave_nomina': fields.selection([('0001','0001'),
                                          ('0002','0002')], 'TSS Clave Nomina', required=True),
        'pay_vacation': fields.boolean('Incluir Vacaciones'),
    }

hr_payslip()

class hr_payslip_run(orm.Model):

    _name = 'hr.payslip.run'
    _inherit = 'hr.payslip.run'

    _columns = {
        'payment_period': fields.selection((('1', 'Primera Quincena'),
                                            ('2', 'Segunda Quincena'),
                                            ('3', 'Fin de mes')), 'Periodo de Pago', required=True),
        'payroll_type': fields.selection([('administrative', 'Administrativa - UAPA'),
                                          ('educational', 'Docente - UAPA'),
                                          ('administrative_ceges_stgo', 'Administrativa - CEGES Santiago'),
                                          ('educational_ceges_stgo', 'Docente - CEGES Santiago'),
                                          ('administrative_ceges_stdo', 'Administrativa - CEGES Santo Domingo'),
                                          ('educational_ceges_stdo', 'Docente - CEGES Santo Domingo'),
                                          ('vacations', 'Vacaciones'),
                                          ('overtime', 'Horas Extras'),
                                          ('xmas_bonus', 'Salario de Navidad')], 'Tipo de Nomina', required=True),
        'clave_nomina': fields.selection([('0001','0001'),
                                          ('0002','0002')], 'TSS Clave Nomina', required=True),
        'type_id': fields.many2one('hr.contract.type', string="Tipo de contrato", required=True,)

    }

hr_payslip_run()

# class hr_salary_rule(orm.Model):
#
#     _inherit = 'hr.salary.rule'
#
#     _columns = {
#         'name_onchange': fields.many2one('hr.contract.news.concepts', required=True, readonly=False, string="Name Concept"),
#     }
#
#     def onchange_name(self, cr, uid, ids, name, context=None):
#         contract_news_concept_obj = self.pool.get('hr.contract.news.concepts')
#         if name:
#             news_concept_name = contract_news_concept_obj.browse(
#                 cr, uid, name, context=None)
#             return {'value': {'name': news_concept_name.name,
#                               'code': news_concept_name.code,
#                               'category_id': news_concept_name.category_id.id}}
#         else:
#             return {}
#
# hr_salary_rule()

class ProffesionalFormation(orm.Model):

    _name = 'hr.employee.formation'
    _columns = {
        'employee_id': fields.many2one('hr.employee', 'Employee'),
        'career_id': fields.many2one('hr.recruitment.career', 'Career'),
        'date_start': fields.date('Date start'),
        'date_end': fields.date('Date end'),
        'specialization': fields.char('Specialization', size=128),
        'degree_id': fields.many2one('hr.recruitment.degree', 'Degree')
    }

class ProffesionalDegree(orm.Model):

    _name = 'hr.recruitment.degree'
    _columns = {
        'name': fields.char('Degree', size=16, required=True),
        'sequence': fields.integer('Sequence', size=16)
    }

ProffesionalDegree()
'''
class hr_payslip_employees(osv.osv_memory):
    _inherit = "hr.payslip.employees"
    #_logger = logging.getLogger(__name__)

    def compute_sheet(self, cr, uid, ids, context=None):
        # pdb.set_trace()
        run_pool = self.pool.get('hr.payslip.run')
        if context is None:
            context = {}
        if context.get('active_id'):
            run_data = run_pool.read(cr, uid, context['active_id'], ['payment_period','payroll_type','subsidiary_id'])

        payment_period = run_data.get('payment_period', False)
        payroll_type = run_data.get('payroll_type',False)
        subsidiary_id = run_data.get('subsidiary_id', False)
        subsidiary_id = subsidiary_id and subsidiary_id[0] or False

        if payment_period:
            context = dict(context, payment_period=payment_period)
        if payroll_type:
            context = dict(context, payroll_type=payroll_type)
        if subsidiary_id:
            context = dict(context, subsidiary_id=subsidiary_id)

        return super(hr_payslip_employees, self).compute_sheet(cr, uid, ids, context=context)

    def compute_sheet(self, cr, uid, ids, context=None):
        #res = super(hr_payslip_employees, self).compute_sheet(
        #    cr, uid, ids, context)
        # pdb.set_trace()
        emp_pool = self.pool.get('hr.employee')
        slip_pool = self.pool.get('hr.payslip')
        run_pool = self.pool.get('hr.payslip.run')
        slip_ids = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        run_data = {}
        if context and context.get('active_id', False):
            run_data = run_pool.read(
                cr, uid, context['active_id'], ['date_start', 'date_end', 'credit_note', 'payment_period',
                                                'payroll_type'])
        from_date = run_data.get('date_start', False)
        to_date = run_data.get('date_end', False)
        credit_note = run_data.get('credit_note', False)
        payment_period = run_data.get('payment_period', False)
        payroll_type = run_data.get('payroll_type', False)
        if not data['employee_ids']:
            raise osv.except_osv(
                _("Warning!"), _("You must select employee(s) to generate payslip(s)."))
        for emp in emp_pool.browse(cr, uid, data['employee_ids'], context=context):
            slip_data = slip_pool.onchange_employee_id(
                cr, uid, [], from_date, to_date, emp.id, contract_id=False, context=context)
            res = {
                'employee_id': emp.id,
                'name': slip_data['value'].get('name', False),
                'struct_id': slip_data['value'].get('struct_id', False),
                'contract_id': slip_data['value'].get('contract_id', False),
                'payslip_run_id': context.get('active_id', False),
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids', False)],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids', False)],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': credit_note,
                'payment_period': payment_period,
                'payroll_type': payroll_type,
            }
            slip_ids.append(slip_pool.create(cr, uid, res, context=context))
        slip_pool.compute_sheet(cr, uid, slip_ids, context=context)
        return {'type': 'ir.actions.act_window_close'}

'''
