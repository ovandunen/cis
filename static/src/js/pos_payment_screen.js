odoo.define('pos_cis_vsd.multi_currency_payment', function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const core = require('web.core');

    PaymentScreen.include({
        async validateOrder(isForceValidate) {
            var self = this;

            if (this.order.get_orderlines().length === 0) {
                return self.showPopup('ErrorPopup', {
                    title: 'Keine Artikel',
                    body: 'Sie können keine Zahlung ohne Artikel durchführen.',
                });
            }

            // Währungsprüfung
            var selectedCurrency = this.order.get_selected_currency();
            if (!selectedCurrency) {
                return self.showPopup('ErrorPopup', {
                    title: 'Währung fehlt',
                    body: 'Bitte wählen Sie eine Währung für die Zahlung aus.',
                });
            }

            return this._super(isForceValidate);
        },
    });
});
