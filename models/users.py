from unittest import result
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'res.users'


    @api.model
    def get_team_lead(self, user_id):
        result = False
        result = self.team_leader_id and self.team_leader_id.id
        return result