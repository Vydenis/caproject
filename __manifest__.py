# -*- coding: utf-8 -*-
{
    'name': "CodeAcademy project",

    'summary': """
        CodeAcademy odoo course individual project""",

    'description': """
        Projects managment tool for:
            - projects
            - jobs
            - employees
            - invoices
    """,

    'author': "Vydenis",
    'website': "-",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_view.xml',
        'views/jobs_view.xml',
        'views/bills_view.xml',
        'views/partner_inherintanced_view.xml',
        'views/employee_inherintanced_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
