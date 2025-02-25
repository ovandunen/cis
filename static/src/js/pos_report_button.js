odoo.define('pos_cis_vsd.report_button', function (require) {
    "use strict";

    const screens = require('point_of_sale.screens');
    const core = require('web.core');
    const QWeb = core.qweb;

    screens.ActionButtonWidget.include({
        button_click: function () {
            this._super();
            var self = this;

            // Zeigt den X- oder Z-Bericht an
            this.pos.generate_z_report().then(function (report) {
                self.show_popup('text', {
                    title: 'Z-Bericht',
                    body: QWeb.render('ZReportTemplate', {report: report}),
                });
            });
        },
    });
});
