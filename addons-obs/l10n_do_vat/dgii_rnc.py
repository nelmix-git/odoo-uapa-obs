# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 19:37:57 2013

@author: Carlos Llamacho
"""

from openerp.osv import orm, fields
import sqlite3
import logging
from os import path

logger = logging.getLogger(__name__)
'''
class res_partner(orm.Model):
    _name= 'res.partner'
    _inherit= 'res.partner'
    _columns= {
        'vat_type':fields.selection((('personal_id','Personal Id'),
                                     ('rnc', 'RNC')),'Vat type', required= True),
        'rnc':fields.integer('RNC', size=9, help='Tax Identification Number.'),
        'personal_id':fields.char('Personal Identification', size=11, help='Personal Id Number')
    }

    def onchange_personal_id(self, cr, uid, ids, id_number, context=None):
        """Verifies that the personal id is compatible with the Luhm algorithm.

        Arguments:
        id_number - Integer. Positional.

        Returns:
        True if check passed.
        Exception otherwise."""
        id_list = []
        if not id_number:
            return False
        for i in id_number:
            id_list.append(i)
        id_check_digit = id_list[-1]
        id_list = id_list[:-1]
        sum_number = 0

        for number in id_list:
            num_index = id_list.index(number)
            if (num_index + 1) % 2 == 0:
                number = int(number) * 2
                if number > 10:
                    number -= 9
                    sum_number += number
                else:
                    sum_number += number
            else:
                sum_number += int(number)
            id_list[num_index] = '*'
        sum_number = sum_number * 9
        sum_number = str(sum_number)
        sum_check_digit = sum_number[-1]

        if sum_check_digit == id_check_digit:
            return True
        else:
            raise orm.except_orm('Error', 'This personal id does not appear to be valid.')

    def write(self, cr, uid, ids, values, context=None):
        for partner in self.browse(cr, uid, ids, context):
            if values.has_key('personal_id'):
                id_number = values.get('personal_id')
                valid_id = self.onchange_personal_id(cr, uid, partner.id, id_number, context)
                if not values['personal_id']:
                    pass
                elif not valid_id:
                    raise orm.except_orm("Error", "Check that the personal id is a valid number.")
            elif values.has_key('rnc'):
                if not values['rnc']:
                    pass
                elif not self.validate_rnc(cr, uid, [partner.id], context):
                    raise orm.except_orm("Error", "Check that the RNC is a valid number.")


        res = super(res_partner, self).write(cr, uid, ids, values, context)
        return res

    def validate_rnc(self, cr, uid, ids, context=None):
        """Validates the number in the field against a sqlite database with
        the RNC numbers registered in the DGII."""
        db_name = "DGII_RNC.db"
        absolute_path = path.dirname(path.abspath(__file__))
        absolute_path += '/' + db_name
        for partner in self.browse(cr, uid, ids, context):
            prospect_rnc = (partner.rnc, )
            try:
                conn = sqlite3.connect(absolute_path)
                logger.info('Connection succesful.')
                cursor = conn.cursor()
                results = cursor.execute("SELECT number FROM DGII_RNC WHERE number=?", prospect_rnc)
                try:
                    results.next()[0]
                    return True
                except StopIteration, e:
                    raise orm.except_orm('Error',"No RNC registered with this number.")
            except sqlite3.Error, error:
                raise orm.except_orm('Error', error.message)
                logger.error(error.message)

res_partner()
'''

