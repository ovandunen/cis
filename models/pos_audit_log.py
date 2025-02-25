from odoo import models, fields, api

class POSAuditLog(models.Model):
    _name = 'pos.audit.log'
    _description = 'POS Audit Log'

    order_id = fields.Many2one('pos.order', string='POS Order', required=True)
    mrc_code = fields.Char(string='Machine Registration Code', required=True)
    mac_address = fields.Char(string='MAC Address', required=True)
    receipt_type = fields.Selection([
        ('ns', 'Normal Sale'),
        ('nr', 'Refund'),
        ('copy', 'Copy'),
        ('training', 'Training'),
        ('proforma', 'Proforma'),
    ], string='Receipt Type')
    action = fields.Char(string='Action', required=True)
    details = fields.Text(string='Details')
    user_id = fields.Many2one('res.users', string='User', required=True)
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, required=True)

    @api.model
    def log_action(self, order, action, details):
        """ Loggt eine Aktion im Zusammenhang mit einem POS-Auftrag """
        self.create({
            'order_id': order.id,
            'mrc_code': order.mrc_code,
            'mac_address': order.mac_address,
            'receipt_type': order.receipt_type,
            'action': action,
            'details': details,
            'user_id': self.env.uid,
        })

