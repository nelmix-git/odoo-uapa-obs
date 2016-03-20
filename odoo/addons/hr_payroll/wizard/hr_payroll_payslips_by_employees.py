# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
from datetime import datetime
from dateutil import relativedelta

from openerp.osv import fields, osv
from openerp.tools.translate import _

class hr_payslip_employees(osv.osv_memory):

    _name ='hr.payslip.employees'
    _description = 'Generate payslips for all selected employees'
    _columns = {
        'employee_ids': fields.many2many('hr.employee', 'hr_employee_group_rel', 'payslip_id', 'employee_id', 'Employees'),
    }

    def get_contract(self, cr, uid, employee, date_from, date_to, context=None):
        """
        @param employee: browse record of employee
        @param date_from: date field
        @param date_to: date field
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        contract_obj = self.pool.get('hr.contract')
        clause = []
        #a contract is valid if it ends between the given dates
        clause_1 = ['&',('date_end', '<=', date_to),('date_end','>=', date_from)]
        #OR if it starts between the given dates
        clause_2 = ['&',('date_start', '<=', date_to),('date_start','>=', date_from)]
        #OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_3 = ['&',('date_start','<=', date_from),'|',('date_end', '=', False),('date_end','>=', date_to)]
        clause_final =  [('employee_id', '=', employee.id),'|','|'] + clause_1 + clause_2 + clause_3
        contract_ids = contract_obj.search(cr, uid, clause_final, context=context)
        return contract_ids

    def compute_sheet(self, cr, uid, ids, context=None):
        # import pdb; pdb.set_trace()
        emp_pool = self.pool.get('hr.employee')
        slip_pool = self.pool.get('hr.payslip')
        run_pool = self.pool.get('hr.payslip.run')
        contract_pool = self.pool.get('hr.contract')

        slip_ids = []
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, context=context)[0]
        run_data = {}
        if context and context.get('active_id', False):
            run_data = run_pool.read(cr, uid, [context['active_id']], ['date_start', 'date_end', 'credit_note',
                                                                       'payment_period','payroll_type',
                                                                       'subsidiary_id', 'clave_nomina','type_id'])[0]
        from_date =  run_data.get('date_start', False)
        to_date = run_data.get('date_end', False)
        credit_note = run_data.get('credit_note', False)
        payment_period = run_data.get('payment_period', False)
        subsidiary_id = run_data.get('subsidiary_id', False)
        payroll_type = run_data.get('payroll_type', False)
        clave_nomina = run_data.get('clave_nomina', False)
        type_id = run_data.get('type_id', False)
        type_id = type_id and type_id[0]
        if not data['employee_ids']:
            raise osv.except_osv(_("Warning!"), _("You must select employee(s) to generate payslip(s)."))

        emp_counter = 0
        for emp in emp_pool.browse(cr, uid, data['employee_ids'], context=context):

            emp_counter += 1
            print "Empleado No. " + str(emp_counter)
            clause = []

            #a contract is valid if it ends between the given dates
            clause_1 = ['&',('date_end', '<=', from_date ),('date_end','>=', to_date)]
            #OR if it starts between the given dates
            clause_2 = ['&',('date_start', '<=', to_date),('date_start','>=', from_date)]
            #OR if it starts before the date_from and finish after the date_end (or never finish)
            clause_3 = ['&',('date_start','<=', from_date),'|',('date_end', '=', False),('date_end','>=', to_date)]
            clause_final =  [('employee_id', '=', emp.id), ('type_id','=', type_id), '|','|']  + clause_1 + clause_2 + clause_3


            contract_search = contract_pool.search(cr, uid, clause_final)
            contract_data = contract_pool.browse(cr, uid, contract_search)

            contract_counter = 0
            for contract in contract_data:

                
                slip_data = slip_pool.onchange_employee_id(cr, uid, [], from_date, to_date, emp.id,
                                                           contract_id=False, context=context)

                
                if contract:
                    contract_counter += 1
                    res = {
                        'employee_id': emp.id,
                        'name': slip_data['value'].get('name', False),
                        'struct_id': contract.struct_id.id,
                        'contract_id': contract.id,
                        'payslip_run_id': context.get('active_id', False),
                        'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids', False)],
                        'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids', False)],
                        'date_from': from_date,
                        'date_to': to_date,
                        'credit_note': credit_note,
                        'payment_period': payment_period,
                        'payroll_type': payroll_type,
                        'subsidiary_id': subsidiary_id and subsidiary_id[0] or False,
                        'clave_nomina': clave_nomina
                    }
                    slip_ids.append(slip_pool.create(cr, uid, res, context=context))
                    print "Contrato No " + str(contract_counter)
        
        slip_pool.compute_sheet(cr, uid, slip_ids, context=context)
        print "Nomina computada"
        return {'type': 'ir.actions.act_window_close'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

