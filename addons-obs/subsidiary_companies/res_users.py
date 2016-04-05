#-*- coding: utf-8 -*-
from openerp.osv import orm, fields


class ResUsers(orm.Model):

    _inherit = 'res.users'
    _columns = {
        'subsidiary_ids': fields.many2many('res.company.subsidiary',
                                           'res_user_subsidiary_rel',
                                           'user_id',
                                           'subsidiary_id',
                                           'Subsidiaries'),
        'subsidiary_id': fields.many2one('res.company.subsidiary',
                                         'Subsidiary', required=True),
    }

    def onchange_subsidiary(self, cr, uid, ids, subsidiary_id, context=None):
        return {'warning':
                {'title':'Subsidiary Switch Warning',
                 'message':"""Please keep in mind that documents currently
                             displayed may not be relevant after switching
                             to another subsidiary. If you have unsaved changes,
                             please make sure to save and close all forms
                             before switching to a different subsidiary.
                             (You can click on Cancel in the User Preferences now)""",
                 }
                }

ResUsers()
