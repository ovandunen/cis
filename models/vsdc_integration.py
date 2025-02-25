from odoo import models, fields  # Sicherstellen, dass models korrekt importiert ist
import logging

_logger = logging.getLogger(__name__)

class VSDCIntegration(models.Model):
    _name = 'vsdc.integration'  # Neues Modell anstatt Erweiterung
    _description = 'VSDC Integration'

    def validate_with_vsdc(self, transaction_data):
        """Synchronisierung der VSDC-Validierung."""
        try:
            vsdc_payload = {
                'transaction_id': transaction_data['order_id'],
                'amount': transaction_data['transaction_data'][0]['amount_total'],
                'date': transaction_data['transaction_data'][0]['date_order'],
                'mrc_code': transaction_data['transaction_data'][0]['mrc_code'],
                'receipt_type': transaction_data['transaction_data'][0]['receipt_type'],
            }
            response = self._send_to_vsdc_server(vsdc_payload)
            if not response.get('status') == 'success':
                raise ValueError("VSDC-Validierung fehlgeschlagen: {}".format(response.get('error')))
            return True
        except Exception as e:
            _logger.error("VSDC-Validierungsfehler: %s", str(e))
            return False

    def validate_with_vsdc_async(self, transaction_data):
        """Asynchrone VSDC-Validierung."""
        # Derzeit als normale Methode aufgerufen, bis das `queue_job`-Modul korrekt funktioniert
        return self.validate_with_vsdc(transaction_data)

    def _send_to_vsdc_server(self, payload):
        _logger.info("Sende Daten an VSDC: %s", payload)
        if payload['mrc_code'] != 'VALID_MRC_CODE':
            return {'status': 'error', 'error': 'Ungültiger MRC-Code'}
        return {'status': 'success'}

