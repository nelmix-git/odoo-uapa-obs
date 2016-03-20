# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {year} {developer} (<{mail}>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

{
    'name': "HR Employee Updates",
    'version': '1.0',
    'category': 'Human Resources',
    'description': """Creacion de Numero Cuenta Bancaria""",
    'author': 'OBS, Yasmany Castillo - yasmany.castillo@obsdr.com.do',
    'website': '',
    'license': 'AGPL-3',
    "depends": ['base',
                'hr',],
    "data": ['hr_employee_views.xml',],
    "active": False,
    "installable": True
}
