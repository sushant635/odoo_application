# -*- encoding: utf-8 -*-

{
    'name': 'CRM addons',
    'summary': """
        An easy way to attach a file to your survey. This functionality is realized through choosing the type of questions beforehand; then uploading the file.""",
    'version': '14.0',
    'category': 'CRM',
    'description': """
        CRM 
    """,
    'author': 'Fogits Solutions',
    'website': 'https://www.fogits.com/',
    'depends': ['contacts','crm'],
    'images': [],
    'data': [
        'views/ir.model.access.csv',
        'views/addon_crm.xml'

    ],
    'installable': True,
    'application': True,
    'auto_install': True
}
