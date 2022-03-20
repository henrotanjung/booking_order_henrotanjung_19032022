
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean('Is Booking Order?', default=True)
    service_team_id = fields.Many2one('service.team', string='Team', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', 'sale_order_user_rel', 'order_id', 'user_id', string='Team Members', required=True)
    booking_start = fields.Datetime('Booking Start', required=True)
    booking_end = fields.Datetime('Booking End', required=True)
    work_order_count = fields.Integer(string='# of Invoices', compute='_get_work_order', readonly=True)


    @api.depends('state', 'order_line.invoice_status')
    def _get_work_order(self):
        work_order_ids = self.env['work.order'].browse()
        work_order_id = work_order_ids.search([('booking_order_ref','=', self.id)])
        for order in self:
            order.update({
                'work_order_count' : len(work_order_id)
            })
        

    @api.multi
    def action_view_work_order(self):
        work_order_ids = self.env['work.order'].browse()
        work_order_id = work_order_ids.search([('booking_order_ref','=', self.id)])
        if len(work_order_id) > 1:
            domain = [('id', 'in', [order.id for order in work_order_id])]
            return {
                'name': _('Work Order'),
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'work.order',
                'view_id': self.env.ref('booking_order_henrotanjung_19032022.view_work_order_tree').id,
                'type': 'ir.actions.act_window',
                'domain': domain
            }
        if len(work_order_id) == 1:
            return {
                    'name': _('Work Order'),
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'work.order',
                    'view_id': self.env.ref('booking_order_henrotanjung_19032022.view_work_order_form').id,
                    'type': 'ir.actions.act_window',
                    'res_id': work_order_id.id,
                    'context': work_order_id.id,
                }

    @api.onchange('service_team_id')     
    def onchange_team_id(self):
        if self.service_team_id:
            self.team_leader_id = self.env['service.team'].get_team_lead(self.service_team_id)
            # self.team_member_ids = [(6, 0, [1,3])]
            self.team_member_ids = self.env['service.team'].get_team_member(self.service_team_id)

    def get_overlap(self, work_order_ids):
        result = {'overlap': False,
                    'ref': ''}

        for work_order in work_order_ids:
            if work_order.state not in ('cancelled','done'):
                if ((self.booking_start >= work_order.planned_start and self.booking_start <= work_order.planned_end) or (self.booking_end >= work_order.planned_start and self.booking_end <= work_order.planned_end)):
                    result['overlap'] = True
                    result['ref'] = work_order.booking_order_ref.name
                    return result

    def check_work_order_overlap(self):
        team_leader_id = self.team_leader_id
        member_ids = self.team_member_ids
        work_order_ids = self.env['work.order'].browse()
        work_order_ids += work_order_ids.search(['|', ('team_leader_id', '=', team_leader_id.id), ('team_member_ids', 'in', [member_id.id for member_id in self.team_member_ids])])

        if not work_order_ids:
            raise Warning("Team is available for booking")
        
        {'domain': {'item_delivered_ids': [('order_id', '=', self.id)]}}
        overlap_data = self.get_overlap(work_order_ids)
        # print ('over_lapppppppp', overlap_data)
        if overlap_data:
            raise Warning("Team already has work order during that period on %s"%(overlap_data.get('ref'),))
        elif not overlap_data:
            raise Warning("Team is available for booking")

    def check_work_order_overlap_confirm(self):
        team_leader_id = self.team_leader_id
        member_ids = self.team_member_ids
        work_order_ids = self.env['work.order'].browse()
        work_order_ids += work_order_ids.search(['|', ('team_leader_id', '=', team_leader_id.id), ('team_member_ids', 'in', [member_id.id for member_id in self.team_member_ids])])

        overlap_data = self.get_overlap(work_order_ids)
        if overlap_data:
            raise Warning("Team is not available during this period, already booked on SOXX. Please book on another date.")

    def create_work_order(self, vals, order_created=False):
        work_order_obj = self.env['work.order']

        if type(vals) is dict:
            work_order_vals = {'service_team_id': vals['service_team_id'], 'team_leader_id': vals['team_leader_id'], 'team_member_ids': vals['team_member_ids'], 'planned_start': vals['booking_start'], 'planned_end': vals['booking_end'], 'booking_order_ref': order_created.id, 'state': 'pending'}
            work_order_result = work_order_obj.create(work_order_vals)
            print ('work_order_result', work_order_result)
            return work_order_result

        elif type(vals) is not dict:
            work_order_vals = {'service_team_id': vals.service_team_id.id, 'team_leader_id': vals.team_leader_id.id, 'team_member_ids': vals.team_member_ids, 'planned_start': vals.booking_start, 'planned_end': vals.booking_end, 'booking_order_ref': vals.id, 'state': 'pending'}
            work_order_result = work_order_obj.create(work_order_vals)

            return work_order_result

        
    @api.model
    def create(self, vals):
        
        # self.check_work_order_overlap()
        
        result = super(SaleOrder, self).create(vals)
        # self.create_work_order(vals, result)    
        
        return result

    @api.multi
    def action_confirm(self):
        self.check_work_order_overlap_confirm()
        super(SaleOrder, self).action_confirm()
        self.create_work_order(self)  

        return True

    
        
        

    

        
