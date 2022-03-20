from odoo import api, fields, models
from datetime import datetime


class WorkOrder(models.Model):
    _name = 'work.order'

    name = fields.Char(string='WO Number', readonly=True, default='/')
    booking_order_ref = fields.Many2one('sale.order', string='Booking Order Reference', readonly=True)
    service_team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', 'work_order_user_rel', 'work_id', 'user_id', string='Team Members')
    planned_start = fields.Datetime('Planned Start', required=True)
    planned_end = fields.Datetime('Planned End', required=True)
    date_start = fields.Datetime('Date Start', readonly=True)
    date_end = fields.Datetime('Date End', readonly=True)
    state = fields.Selection([('pending', 'Pending'), ('in_progress', 'In Progress'), ('done', 'Done'), ('cancelled', 'Cancelled')],default='pending', string='State', readonly=True, copy=False, store=True)
    description = fields.Text('Notes')
    

    @api.model
    def create(self, vals):
        obj = super(WorkOrder, self).create(vals)
        if obj.name == '/':
            seq_number = self.env['ir.sequence'].get('work.order.code') or '/'
            obj.write({'name': seq_number})
        return obj

    @api.multi
    def copy(self, default=None):
        default = default or {}                
        result = super(WorkOrder, self).copy(default)
        seq_number = self.env['ir.sequence'].get('work.order.code') or '/'
        result.write({'name': seq_number})
        return result

    @api.multi
    def start_work(self):
        self.update({'state': 'in_progress', 'date_start': datetime.now()})
        return True

    @api.multi
    def end_work(self):
        self.update({'state': 'done', 'date_end': datetime.now()})
        return True
    
    @api.multi
    def reset(self):
        self.update({'state': 'pending', 'date_start': False})
        return True

    # @api.multi
    # def cancel(self):
    #     self.update({'state': 'cancelled'})
    #     return True