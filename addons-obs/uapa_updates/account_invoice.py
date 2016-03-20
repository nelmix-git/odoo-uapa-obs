#-*- coding: utf-8 -*-

"""
Created on Tue Jul 25

@author: Carlos Llamacho
"""

from openerp.osv import fields, orm
"""
class account_invoice(orm.Model):
    _inherit = 'account.invoice'

    _columns = {
	'fiscal_clasification' : fields.selection((
			('01 - GASTOS DE PERSONAL','01 - GASTOS DE PERSONAL'), 
			('02 - GASTOS POR TRABAJOS, SUMINISTROS Y SERVICIOS','02 - GASTOS POR TRABAJOS, SUMINISTROS Y SERVICIOS'),
			('03 - ARRENDAMIENTOS','03 - ARRENDAMIENTOS'),
			('04 - GASTOS DE ACTIVOS FIJOS','04 - GASTOS DE ACTIVOS FIJOS'),
			('05 - GASTOS DE REPRESENTACION','05 - GASTOS DE REPRESENTACION'),
			('06 - OTRAS DEDUCCIONES ADMITIDAS','06 - OTRAS DEDUCCIONES ADMITIDAS'),
			('07 - GASTOS FINANCIEROS','07 - GASTOS FINANCIEROS'),
			('08 - GASTOS EXTRAORDINARIOS','08 - GASTOS EXTRAORDINARIOS'),
			('09 - COMPRAS QUE FORMAN PARTE DEL COSTO DE VENTA','09 - COMPRAS QUE FORMAN PARTE DEL COSTO DE VENTA'),
			('10 - ADQUISICIONES DE ACTIVOS','10 - ADQUISICIONES DE ACTIVOS'),
			('11 - GASTOS DE SEGURO','11 - GASTOS DE SEGURO')),
			'Clasicacion Fiscal de Compra', required=True, readonly=True, states={'draft':[('readonly',False)]}),
	}

account_invoice()
"""
