{
    'name': 'SU Dynamic ListView Odoo 10',
    'summary': 'SU Dynamic ListView Odoo 10',
    'version': '1.0',
    'category': 'Web',
    'description': """
        SU Dynamic ListView Odoo 10
    """,
    'author': "startup",
    'depends': ['web'],
    'data': [
        'views/templates.xml',
        'security/show_fields_security.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'images': ['images/main_screen.jpg'],
    'price': 250,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': False,
    'images': [
        'static/description/module_image.png',
    ],
}
