from odoo import models, fields
import uuid
from odoo.exceptions import ValidationError

class POSConfig(models.Model):
    _inherit = 'pos.config'

    mrc_code = fields.Char(string='Machine Registration Code', required=True, help="Eindeutiger Registrierungscode für dieses POS-Terminal.")
    mac_address = fields.Char(string='MAC-Adresse', default=lambda self: self._get_mac_address(), help="MAC-Adresse des Geräts.")
    available_currencies = fields.Many2many('res.currency', string='Verfügbare Währungen')

    def _get_mac_address(self):
        mac = uuid.getnode()
        return ':'.join(['{:02x}'.format((mac >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])

    def register_mrc_code(self, mrc_code):
        """ Methode zur Registrierung des MRC-Codes und der MAC-Adresse """
        self.mrc_code = mrc_code
        self.mac_address = self._get_mac_address()
        return True

    def validate_mac_and_mrc(self):
        """ Überprüft die MAC-Adresse und den MRC-Code """
        if self.mac_address != self._get_mac_address():
            return False
        return True
