#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class HrContract(orm.Model):

    _inherit = 'hr.contract'
    _auto = True
    _columns = {
        'schedule_pay': fields.selection((('fortnightly', 'Quincenal'),
                                          ('monthly', 'Mensual'),
                                          ('quarterly', 'Trimestral'),
                                          ('semi-annually', 'Semestral'),
                                          ('annually', 'Anual'),
                                          ('weekly', 'Semanal'),
                                          ('bi-weekly', 'Bi-semanal'),
                                          ('bi-monthly', 'Bi-mensual')), 'Scheduled Pay', required=True)
    }


