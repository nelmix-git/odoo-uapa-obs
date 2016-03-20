# -*- coding: utf-8 -*-

from openerp.osv import fields, osv, orm
import logging

class hr_employee(orm.Model):
	
	_inherit = "hr.employee"	
	
	def employee_bank_association(self, cr, uid, context=None):
		#from ipdb import set_trace; set_trace()
		logging.getLogger(self._name).info("\nStarting employee_bank_association cron job.\n")
		employee = self.pool.get('hr.employee')
		partner = self.pool.get('res.partner')
		bank = self.pool.get('res.partner.bank')		
		args = []
		res = {}
		partner_id = 0
		values = {}
		secuencia = []
		search = employee.search(cr, uid, args)
		employee_id = employee.read(cr, uid, search, ['id', 'name', 'address_home_id', 'bank_account_id'])
		
		for row in employee_id:
			secuencia.append(row.__getitem__('id') )
			for r in self.browse(cr, uid, secuencia, context=context):
				res['address_home_id'] = r.address_home_id.id
			
				if res['address_home_id']:
					logging.getLogger(self._name).info("""\nSocio ya creado!\n""")
				else:
					for e_record in employee.browse(cr, uid, secuencia, context):
						res['name']  = e_record.name
						
						if e_record.address_home_id.id:	
							logging.getLogger(self._name).info("""\nSocio ya creado!\n""")
						else:
							partner.create(cr, uid, {'name': res['name']})
				
			for e_record in employee.browse(cr, uid, secuencia, context):
					name = e_record.name.encode('utf-8')
					res['name']  = name
			
			cr.execute("SELECT id FROM res_partner WHERE name = '{0}'".format(res['name']))
			res['partner_id'] = cr.fetchmany()
					
			for b_record in bank.browse(cr, uid, secuencia, context=context):
				bank_type_obj = self.pool.get('res.partner.bank.type')
		
				result = []
				type_ids = bank_type_obj.search(cr, uid, [])
				bank_types = bank_type_obj.browse(cr, uid, type_ids, context=context)
				for bank_type in bank_types:
					result.append((bank_type.code, bank_type.name))
				
				values.update({
					'state' : str(result[0][0]),
					'acc_number' : '00000',
					'partner_id' : res['partner_id'][0][0],				
				})
				
				bank.create(cr, uid, values)
				break
						
			cr.execute("SELECT id FROM res_partner_bank WHERE partner_id = {}".format(res['partner_id'][0][0]))
			res['bank_id'] = cr.fetchmany()
			employee.write(cr, uid, secuencia, {'address_home_id' : res['partner_id'][0][0],'bank_account_id':res['bank_id'][0][0]})		
			secuencia.remove(row.__getitem__('id'))
			logging.getLogger(self._name).info("""\nAccion exitosa\n""")
		
		logging.getLogger(self._name).info("""\n****************Fin Cron Job************************\n""")
		return employee
	
hr_employee()
