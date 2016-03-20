# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Open Business Solutions (<http://www.obsdr.com>)
#    Author: Ernesto Mendez
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
import time
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp.exceptions import Warning
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class payroll_header_parameters(models.Model):
    _name = 'payroll.header.parameters'
    _description = 'Parametros de Encabezados de Nomina'

    bank_id: fields.Many2one('res.bank', 'Bank', required=True, readonly=False)
    payroll_type: fields.Selection([('administrative', 'Administrativa - UAPA'),
                                          ('educational', 'Docente - UAPA'),
                                          ('administrative_ceges_stgo', 'Administrativa - CEGES Santiago'),
                                          ('educational_ceges_stgo', 'Docente - CEGES Santiago'),
                                          ('administrative_ceges_stdo', 'Administrativa - CEGES Santo Domingo'),
                                          ('educational_ceges_stdo', 'Docente - CEGES Santo Domingo'),
                                          ('vacations', 'Vacaciones'),
                                          ('overtime', 'Horas Extras'),
                                          ('xmas_bonus', 'Salario de Navidad')], 'Tipo de Nomina', required=True)
    subsidiary_id: fields.Many2one('res.company.subsidiary', 'Subsidiary', required=True, readonly=False)
    journal_id: fields.Many2one('account.journal', 'Diario de Salarios', domain=[('is_salary_journal','=',True)])


