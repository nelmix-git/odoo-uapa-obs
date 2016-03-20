# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 14:08:50 2013

@author: Carlos Llamacho
"""

from openerp.osv import orm, fields



class event_event(orm.Model):
    _name="event.event"
    _inherit="event.event"

    _columns = {
    "is_training":fields.boolean("Training?", help="Select this field if this event falls into the employee improvement program."),
    "expenses_ids":fields.one2many('hr.expense.expense', 'event_id', "Expenses")
    }

event_event()

class event_registration(orm.Model):
    _name="event.registration"
    _inherit="event.registration"

    _columns = {
    'employee_id':fields.many2one('hr.employee', 'Employee')
    }

    def onchange_employee_id(self, cr, uid, ids, employee_id, context=None):
        emp_obj = self.pool.get("hr.employee")
        if employee_id:
            employee = emp_obj.browse(cr, uid, employee_id, context=None)
            return {'value':{'name':employee.name, 'phone':employee.work_phone, 'email':employee.work_email}}
        else:
            return {}

event_registration()

