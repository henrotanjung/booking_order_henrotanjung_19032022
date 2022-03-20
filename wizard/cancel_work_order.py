# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class CancelWorkOrder(models.TransientModel):
    _name = "cancel.work.order"
    _description = "Cancel Work Order "

    reason = fields.Text('Reason for cancellation', required=True)

    
    @api.multi
    def submit_cancelled(self):
        work_orders = self.env['work.order'].browse(self._context.get('active_ids', []))
        current_notes_value = work_orders.description
        print('ccurentnt notes', current_notes_value)
        print ('reasonnnn', self.reason)
        current_notes_value = current_notes_value or '' + self.reason or ''
        work_orders.update({'state': 'cancelled', 'description': current_notes_value})

        return True

    