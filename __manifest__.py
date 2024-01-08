{
    'name': 'Estate',
    'version': '0.1',
    'category': 'Sales',
    'description': "Module estate",
    'depends': [
        "base"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_menus.xml',
    ],
    'installable': True,
    'application': True,
}