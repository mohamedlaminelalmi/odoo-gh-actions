# -*- coding: utf-8 -*-
{
    'name': 'Website Product Sticky Details',
    'version': '1.0.0',
    'category': 'Website/Website',
    'depends': ['website_sale'],
    'description': """
    This module add a website feature to display sticky details on the bottom of the product page.
    """,
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
    'assets': {
        'web.assets_frontend': [
            'abt_website_sale_product_sticky_details/static/src/scss/style.scss',
            'abt_website_sale_product_sticky_details/static/src/js/sticky_product_details.js',
        ],
    },
    'license': 'LGPL-3',
    'author': 'Alpha Brains Technologies',
    'website': 'https://www.alpha-brains.dz',
    'price': 25.0,
    'currency': 'EUR',
}
