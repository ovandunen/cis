import base64
import qrcode
from io import BytesIO
from odoo import models, fields, api


class POSOrder(models.Model):
    _inherit = 'pos.order'

    currency_id = fields.Many2one(
        'res.currency',
        string="Order Currency",
        readonly=True,
        default=lambda self: self.env.company.currency_id
    )
    multi_currency_payments = fields.One2many(
        'pos.payment',
        'pos_order_id',
        string="Multi-Currency Payments"
    )
    amount_paid = fields.Monetary(
        string="Paid Amount",
        currency_field='currency_id',
        compute="_compute_amount_paid",
        store=True
    )
    qr_code_image = fields.Binary(
        string="QR Code",
        compute="_compute_qr_code_image",
        store=True
    )

    @api.depends('multi_currency_payments.amount_converted')
    def _compute_amount_paid(self):
        """Berechnet den Gesamtbetrag der Zahlungen in der Bestellwährung."""
        for order in self:
            order.amount_paid = sum(order.multi_currency_payments.mapped('amount_converted'))

    @api.depends('name')
    def _compute_qr_code_image(self):
        """Generiert den QR-Code für die Bestellung als Bild basierend auf der Bestellreferenz."""
        for order in self:
            if order.name:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(order.name)  # QR-Code-Daten basierend auf der Bestellreferenz
                qr.make(fit=True)
                img = qr.make_image(fill='black', back_color='white')
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                order.qr_code_image = base64.b64encode(buffer.getvalue()).decode('ascii')
            else:
                order.qr_code_image = False

    @api.model
    def _process_payment(self, payment_data):
        """Verarbeitet die Zahlung und rechnet die Währung um, wenn nötig."""
        payment = self.env['pos.payment'].create({
            'pos_order_id': self.id,
            'amount': payment_data['amount'],
            'payment_date': fields.Datetime.now(),
            'payment_method_id': payment_data['payment_method_id'],
            'currency_id': payment_data.get('currency_id', self.currency_id.id),  # Setze die Währung
        })

        # Währungsumrechnung, falls nötig
        if payment.currency_id != self.currency_id:
            payment.amount_converted = payment.currency_id._convert(
                payment.amount,
                self.currency_id,
                self.env.company,
                payment.payment_date
            )
        else:
            payment.amount_converted = payment.amount

        # Aktualisiere den bezahlten Betrag
        self.amount_paid = sum(self.multi_currency_payments.mapped('amount_converted'))
        return payment


class POSPayment(models.Model):
    _inherit = 'pos.payment'

    currency_id = fields.Many2one(
        'res.currency',
        string="Payment Currency",
        readonly=True
    )
    amount_converted = fields.Monetary(
        string="Converted Amount",
        currency_field='currency_id',
        readonly=True
    )
    pos_order_currency_id = fields.Many2one(
        'res.currency',
        related='pos_order_id.currency_id',
        readonly=True
    )
