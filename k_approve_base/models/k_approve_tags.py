# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KApproveTags(models.Model):
    _name = 'kapprove.doc.tag'
    _description = "Approval Tags"
    _rec_name = 'name'

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer('Color Index', default=0)
