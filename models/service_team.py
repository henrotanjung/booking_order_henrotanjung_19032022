
from odoo import api, fields, models


class ServiceTeam(models.Model):
    _name = 'service.team'


    name = fields.Char('Team Name', required=True)
    team_leader_id = fields.Many2one('res.users', string='Team Leader', required=True)
    team_member_ids = fields.Many2many('res.users', 'service_team_user_rel', 'team_id', 'user_id', string='Team Members')

    @api.model
    def get_team_lead(self, user_id):
        result = user_id.team_leader_id and user_id.team_leader_id.id
        return result

    @api.model
    def get_team_member(self, user_id):
        result = [m.id for m in user_id.team_member_ids]
        return result