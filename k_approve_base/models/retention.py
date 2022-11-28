from odoo import models, fields, api


class KApproveRetention(models.Model):
    _name = 'kapprove.retention'
    _description = "Retention Period"
    _rec_name = 'name'

    name = fields.Char(string="Name")
    period = fields.Integer(string="Period")
    permanent = fields.Boolean(string="Active")
    date_period = fields.Selection([('days', 'Days'), ('months', 'Months'), ('years', 'Years')], "Date period", default="days")

    @api.onchange('name', 'date_period')
    def onchange(self):
        self.name = str(self.period) + ' ' + self.date_period
