# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Author: Naresh Soni
#    Copyright 2016 Cozy Business Solutions Pvt.Ltd(<http://www.cozybizs.com>)
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


{   'name': 'POS payment Extension',
    'version': '1.0',
   'category': 'Point Of Sale',
    'author' : 'Naresh Soni',
    'website' : 'http://www.cozybizs.com',
    'description': """
This module add new features to the POS
==============================================================================

* Add payment related fields on POS interface

    """,
    'depends': ['marcos_pos'],

    'data': [
        'views/pos_view.xml',
        'template.xml'
    ],
    'qweb': [
        'static/src/xml/pos_payment.xml',
    ],
}
