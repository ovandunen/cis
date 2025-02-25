{
    'name': 'CIS Reporting',
    'version': '1.9',
    'category': 'Point of Sale',
    'summary': 'POS system with CIS, TIN display, company VAT, inventory control, VSDC communication, X and Z reports, QR code on receipts, Multi-Currency Payments, and MRC Registration.',
    'depends': [
        'point_of_sale',
        'queue_job',
        'account',
        'stock',
        'base',
        'bus',
    ],
    'qweb': [
        'static/src/xml/pos_receipt.xml',
        'static/src/xml/pos_report_template.xml',
        'static/src/xml/pos_config_currency.xml',  

    ],
    'data': [
        'views/assets.xml',
        'security/ir.model.access.csv',
        'data/bus_channel.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_cis_vsd/static/src/js/pos_registration.js',
            'pos_cis_vsd/static/src/js/pos_report_button.js',
            'pos_cis_vsd/static/src/js/pos_payment_screen.js',  
            'pos_cis_vsd/static/src/js/currency_selection.js',   
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
