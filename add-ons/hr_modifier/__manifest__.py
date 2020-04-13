# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Employees Modifier',
    'version': '0.1',
    'category': 'Human Resources/Employees',
    'summary': 'Cutomize Employee Module for our purposes',
    
    'depends': [
        'base', 'hr', 'hr_skills'
    ],
    'data': [
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/hr_job_views.xml',
        'views/hr_plan_views.xml',
        'views/hr_employee_category_views.xml',
        'views/hr_employee_public_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_department_views.xml',
        'views/hr_employee_classification_views.xml',
        'views/hr_employee_region_views.xml',
        'views/hr_views.xml',
        'views/mail_channel_views.xml'
    ],
    'qweb': [
        'static/src/xml/chatter.xml',
        'static/src/xml/systray.xml'
    ],
    'installable': True,
    'application': False,
}
