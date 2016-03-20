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

from openerp.tools.translate import _
from openerp.osv import fields, osv

class account_check_write_br_stgo_2500014201(osv.osv_memory):
    _name = 'account.check.write.br.stgo.2500014201'
    _description = 'Imprimir Cheques Banco de Reservas Santiago- Cta 2500014201'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_br_stgo_2500014201(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_br_stgo_2500014201')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_br_stgo_2500014201,
   }

    def print_check_write_br_stgo_2500014201(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_br_stgo_2500014201')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_br', data=data, context=context
        )

class account_check_write_bhd_stgo_02392840012(osv.osv_memory):
    _name = 'account.check.write.bhd.stgo.02392840012'
    _description = 'Imprimir Cheques BHD Santiago - Cta 02392840012'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_stgo_02392840012(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_stgo_02392840012')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_stgo_02392840012,
   }

    def print_check_write_bhd_stgo_02392840012(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_stgo_02392840012')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            #if check.number:
            #    raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_bhd_stdo_02392840047(osv.osv_memory):
    _name = 'account.check.write.bhd.stdo.02392840047'
    _description = 'Imprimir Cheques BHD Santo Domingo - Cta 02392840047'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_stdo_02392840047(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_stdo_02392840047')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_stdo_02392840047,
   }

    def print_check_write_bhd_stdo_02392840047(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_stdo_02392840047')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_br_ng_2500045417(osv.osv_memory):
    _name = 'account.check.write.br.ng.2500045417'
    _description = 'Imprimir Cheques Banco de Reservas Nagua - Cta 2500045417'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_br_ng_2500045417(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_br_ng_2500045417')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_br_ng_2500045417,
   }

    def print_check_write_br_ng_2500045417(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_br_ng_2500045417')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_br', data=data, context=context
        )

class account_check_write_bhd_leon_ec_2392840063(osv.osv_memory):
    _name = 'account.check.write.bhd.leon.ec.2392840063'
    _description = 'Imprimir Cheques BHD Leon Economato - Cta 2392840063'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_leon_ec_2392840063(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_leon_ec_2392840063')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_leon_ec_2392840063,
   }

    def print_check_write_bhd_leon_ec_2392840063(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_leon_ec_2392840063')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_bhd_leon_ceg_stgo_17843860022(osv.osv_memory):
    _name = 'account.check.write.bhd.leon.ceg.stgo.17843860022'
    _description = 'Imprimir Cheques BHD Leon CEGES Santiago - Cta 17843860022'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_leon_ceg_stgo_17843860022(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_leon_ceg_stgo_17843860022')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_leon_ceg_stgo_17843860022,
   }

    def print_check_write_bhd_leon_ceg_stgo_17843860022(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_leon_ceg_stgo_17843860022')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_bhd_leon_ceg_stdo_17843860014(osv.osv_memory):
    _name = 'account.check.write.bhd.leon.ceg.stdo.17843860014'
    _description = 'Imprimir Cheques BHD Leon CEGES Santo Domingo - Cta 17843860014'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_leon_ceg_stdo_17843860014(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_leon_ceg_stdo_17843860014')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_leon_ceg_stdo_17843860014,
   }

    def print_check_write_bhd_leon_ceg_stdo_17843860014(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_leon_ceg_stdo_17843860014')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_bhd_us_2392840055(osv.osv_memory):
    _name = 'account.check.write.bhd.us.2392840055'
    _description = 'Imprimir Cheques BHD - Leon US$ - Cta 2392840055'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_us_2392840055(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_us_2392840055')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_us_2392840055,
   }

    def print_check_write_bhd_us_2392840055(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_us_2392840055')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_bhd_fupuapa_13823040015(osv.osv_memory):
    _name = 'account.check.write.bhd.fupuapa.13823040015'
    _description = 'Imprimir Cheques BHD - Leon FUPUAPA - Cta 13823040015'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bhd_fupuapa_13823040015(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_fupuapa_13823040015')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bhd_fupuapa_13823040015,
   }

    def print_check_write_bhd_fupuapa_13823040015(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bhd_fupuapa_13823040015')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bhd_leon', data=data, context=context
        )

class account_check_write_bpd_inc_790162606(osv.osv_memory):
    _name = 'account.check.write.bpd.inc.790162606'
    _description = 'Imprimir Cheques Banco Popular - Incapre - Cta 790162606'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bpd_inc_790162606(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bpd_inc_790162606')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bpd_inc_790162606,
   }

    def print_check_write_bpd_inc_790162606(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bpd_inc_790162606')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bpd', data=data, context=context
        )

class account_check_write_bpd_uapa_790162770(osv.osv_memory):
    _name = 'account.check.write.bpd.uapa.790162770'
    _description = 'Imprimir Cheques Banco Popular - UAPA - Cta 790162770'

    _columns = {
        'check_number': fields.integer('Next Check Number', required=True, help="The number of the next check number to be printed."),
    }

    def _get_next_number_bpd_uapa_790162770(self, cr, uid, context=None):
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bpd_uapa_790162770')
        return self.pool.get('ir.sequence').read(cr, uid, [sequence_id], ['number_next'])[0]['number_next']

    _defaults = {
        'check_number': _get_next_number_bpd_uapa_790162770,
   }

    def print_check_write_bpd_uapa_790162770(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        voucher_obj = self.pool.get('account.voucher')
        ir_sequence_obj = self.pool.get('ir.sequence')

        #update the sequence to number the checks from the value encoded in the wizard
        dummy, sequence_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_custom_check_writing', 'sequence_check_number_bpd_inc_790162606')
        increment = ir_sequence_obj.read(cr, uid, [sequence_id], ['number_increment'])[0]['number_increment']
        new_value = self.browse(cr, uid, ids[0], context=context).check_number
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #validate the checks so that they get a number
        voucher_ids = context.get('active_ids', [])
        for check in voucher_obj.browse(cr, uid, voucher_ids, context=context):
            new_value += increment
            if check.number:
                raise osv.except_osv(_('Error!'),_("One of the printed check already got a number."))
        voucher_obj.proforma_voucher(cr, uid, voucher_ids, context=context)

        #update the sequence again (because the assignation using next_val was made during the same transaction of
        #the first update of sequence)
        ir_sequence_obj.write(cr, uid, sequence_id, {'number_next': new_value})

        #print the checks
        data = {
            'id': voucher_ids and voucher_ids[0],
            'ids': voucher_ids,
        }

        return self.pool['report'].get_action(
            cr, uid, [], 'account_custom_check_writing.report_check_bpd', data=data, context=context
        )
