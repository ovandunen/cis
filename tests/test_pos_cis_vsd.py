from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestPOSMultiCurrencyMRC(TransactionCase):

    def setUp(self):
        super(TestPOSMultiCurrencyMRC, self).setUp()
        self.pos_config = self.env['pos.config'].create({
            'name': 'Test POS',
        })

    def test_mrc_registration(self):
        """Testet die Registrierung des MRC-Codes und der MAC-Adresse."""
        self.pos_config.register_mrc_code('VALID_MRC_CODE')
        self.assertEqual(self.pos_config.mrc_code, 'VALID_MRC_CODE')
        self.assertTrue(self.pos_config.mac_address)

    def test_mrc_validation_success(self):
        """Testet die erfolgreiche Validierung von MAC-Adresse und MRC-Code."""
        self.pos_config.mac_address = self.pos_config._get_mac_address()  # Setze korrekte MAC
        self.pos_config.mrc_code = 'VALID_MRC_CODE'
        self.assertTrue(self.pos_config.validate_mac_and_mrc())

    def test_mrc_validation_failure(self):
        """Testet die Validierung, wenn die MAC-Adresse nicht übereinstimmt."""
        self.pos_config.mac_address = 'AA:BB:CC:DD:EE:FF'  # Setze falsche MAC-Adresse
        self.pos_config.mrc_code = 'VALID_MRC_CODE'
        self.assertFalse(self.pos_config.validate_mac_and_mrc())

    def test_multi_currency_payment(self):
        """Testet die Multi-Währungs-Zahlung."""
        order = self.env['pos.order'].create({
            'name': 'Test Order',
            'session_id': self.env.ref('point_of_sale.pos_session_default').id,
            'amount_total': 100.0,
        })

        usd_currency = self.env.ref('base.USD')
        eur_currency = self.env.ref('base.EUR')

        payment_data_usd = {
            'amount': 50,
            'payment_method_id': self.env.ref('pos.payment_method_cash').id,
            'currency_id': usd_currency.id,
        }

        payment_data_eur = {
            'amount': 50,
            'payment_method_id': self.env.ref('pos.payment_method_card').id,
            'currency_id': eur_currency.id,
        }

        order._process_payment(payment_data_usd)
        order._process_payment(payment_data_eur)

        self.assertEqual(order.amount_paid, 100.0)  # Der Gesamtbetrag sollte korrekt sein

    def test_currency_conversion(self):
        """Testet die Umrechnung von Fremdwährungen in die Basiswährung."""
        order = self.env['pos.order'].create({
            'name': 'Test Order with Conversion',
            'session_id': self.env.ref('point_of_sale.pos_session_default').id,
            'currency_id': self.env.ref('base.EUR').id,
            'amount_total': 100.0,
        })

        usd_currency = self.env.ref('base.USD')

        # Zahlung in USD
        payment_data_usd = {
            'amount': 100,
            'payment_method_id': self.env.ref('pos.payment_method_cash').id,
            'currency_id': usd_currency.id,
        }

        # Verarbeite die Zahlung und rechne den Betrag in EUR um
        payment = order._process_payment(payment_data_usd)
        self.assertTrue(payment.amount_converted > 0)  # Umrechnung sollte erfolgen
        self.assertTrue(order.amount_paid > 0)

    def test_x_report_generation(self):
        """Testet die Generierung eines X-Berichts."""
        x_report = self.pos_config.generate_x_report()
        self.assertTrue(x_report['total_sales'] >= 0)
        self.assertTrue(x_report['total_taxes'] >= 0)

    def test_z_report_generation(self):
        """Testet die Generierung eines Z-Berichts."""
        z_report = self.pos_config.generate_z_report()
        self.assertTrue(z_report['total_sales'] >= 0)
        self.assertTrue(z_report['total_taxes'] >= 0)
        self.assertTrue(z_report['total_items_sold'] >= 0)
        self.assertTrue(z_report['total_payments'] >= 0)

    def test_audit_logging(self):
        """Testet die Audit-Protokollierung."""
        self.env['pos.audit.log'].log_action(self.pos_config, 'sale', 'Test sale action')
        audit_log = self.env['pos.audit.log'].search([('order_id', '=', self.pos_config.id)])
        self.assertTrue(audit_log)
        self.assertEqual(audit_log[0].action, 'sale')
        self.assertEqual(audit_log[0].details, 'Test sale action')
