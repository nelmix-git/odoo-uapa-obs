#-*- coding: utf-8 -*-
{
    'name': 'Subsidiary Companies',
    'author': 'OBS',
    'version': '1.0',
    'description':"Module that brings the option to create subsidiary companies.",
    'category': 'Configuration',
    'depends': ['base',
                'stock',
                'sale',
                'purchase',
                'purchase_requisition',
                'account',
                'account_budget'],
    'data': ['subsidiary_company_view.xml',
             'res_users_view.xml',
             'security/res_company_subsidiary_security.xml',
             'security/pos_subsidiary_security.xml'],
    'installable': True
}
