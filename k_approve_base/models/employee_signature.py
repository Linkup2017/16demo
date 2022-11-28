# -*- coding: utf-8 -*-


from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    signature = fields.Image('Signature', help='Signature', copy=False, attachment=True)
