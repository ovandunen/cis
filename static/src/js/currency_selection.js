odoo.define('pos_cis_vsd.currency_selection', function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const core = require('web.core');

    PaymentScreen.include({
        init: function () {
            this._super.apply(this, arguments);
        },

        render_paymentlines: function () {
            this._super();
            var self = this;
            var currencies = this.pos.pos_session.available_currencies;  // Währungen aus der POS-Session holen

            this.$('.paymentline').each(function () {
                var paymentline = self.pos.get_order().paymentlines;
                var currency = currencies.find(c => c.id === paymentline.currency_id);
                $(this).find('.paymentline-currency').text(currency.symbol || currency.name);
            });
        },
    });
});
