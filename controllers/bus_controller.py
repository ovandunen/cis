from odoo import http
from odoo.http import request
import json

class VSDCBusController(http.Controller):

    @http.route('/vsdc/validate', type='json', auth='public')
    def vsdc_validate(self):
        messages = request.env['bus.bus'].poll()
        for message in messages:
            if message.get('channel') == 'vsd_communication':
                transaction_data = json.loads(message['message'])
                result = request.env['vsdc.integration'].validate_with_vsdc(transaction_data)
                order = request.env['pos.order'].browse(transaction_data['order_id'])
                order.vsdc_status = 'validated' if result else 'error'
        return {}

