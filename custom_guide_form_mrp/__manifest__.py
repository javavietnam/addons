# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
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
#################################################################################
{
    'name': "Guide Form Operation",
    'author': 'Tran Trang',
    'category': 'Manufacturing',
    'summary': """Guide Form Operation""",
    'website': '',
    'description': """ """,
    'version': '15.0.1.0',
    'depends': ['mrp'],
    'data': ['views/guider_form_report.xml','views/mrp_routing_workcenter.xml','views/mrp_workorder.xml','views/mrp_report_views_main.xml'],
    'license': 'AGPL-3',    
    'installable': True,
    'application': True,
    'auto_install': False,
}
