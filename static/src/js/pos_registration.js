odoo.define('pos_cis_vsd.pos_registration', function (require) {
    "use strict";

    const models = require('point_of_sale.models');
    const rpc = require('web.rpc');
    const gui = require('point_of_sale.gui');

    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var self = this;
            this._super(session, attributes);

            // Check if MRC code is registered
            this.ready.then(function () {
                if (!self.config.mrc_code) {
                    // Prompt user to enter MRC code
                    self.gui.show_popup('input', {
                        'title': 'MRC-Code eingeben',
                        'value': '',
                        'confirm': function (mrc_code) {
                            return rpc.query({
                                model: 'pos.config',
                                method: 'register_mrc_code',
                                args: [self.config.id, mrc_code],
                            }).then(function () {
                                self.gui.show_popup('info', {
                                    'title': 'Registrierung erfolgreich',
                                    'body': 'Der MRC-Code wurde erfolgreich registriert.',
                                });
                            }).catch(function (error) {
                                console.error('MRC-Registrierung fehlgeschlagen:', error);
                                self.gui.show_popup('error', {
                                    'title': 'Registrierungsfehler',
                                    'body': 'Die Registrierung des MRC-Codes ist fehlgeschlagen. Bitte versuchen Sie es erneut oder kontaktieren Sie den Administrator.',
                                });
                            });
                        },
                    });
                } else {
                    // Validate MAC address and MRC code
                    rpc.query({
                        model: 'pos.config',
                        method: 'validate_mac_and_mrc',
                        args: [self.config.id],
                    }).then(function (result) {
                        if (!result) {
                            self.gui.show_popup('error', {
                                'title': 'Registrierungsfehler',
                                'body': 'Die MAC-Adresse dieses Geräts stimmt nicht mit dem registrierten MRC-Code überein. Bitte kontaktieren Sie den Administrator.',
                            });
                        }
                    }).catch(function (error) {
                        console.error('Registrierungsfehler:', error);
                        self.gui.show_popup('error', {
                            'title': 'Kommunikationsfehler',
                            'body': 'Es gab ein Problem mit der POS-Registrierung. Versuchen Sie es erneut oder kontaktieren Sie den Administrator.',
                        });
                    });
                }
            });
        },
    });
});
