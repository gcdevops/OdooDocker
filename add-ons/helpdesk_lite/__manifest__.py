# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Lite",
    'version': "1.1.1",
    'author': "Golubev",
    'category': "Tools",
    'support': "golubev@svami.in.ua",
    'summary': "A helpdesk / support ticket system",
    'description': """
        Easy to use helpdesk system
        with teams and website portal
    """,
    'license':'LGPL-3',
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/helpdesk_pages.xml',
        'views/helpdesk_tickets.xml',
        'views/helpdesk_team_views.xml',
        'views/helpdesk_stage_views.xml',
        'views/helpdesk_data.xml',
        'views/helpdesk_templates.xml',

    ],
    'demo': [
        'demo/helpdesk_demo.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'depends': ['base', 'mail', 'portal',],
    'application': True,
}