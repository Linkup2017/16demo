# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KApproveCategory(models.Model):
    _name = 'kapprove.category'
    _inherit = ['mail.thread']
    _description = "Approve Category"
    _rec_name = 'complete_name'
    _order = "sequence,id"


    name = fields.Char(string="Category Name", required=True)
    parent_id = fields.Many2one('kapprove.category', string="Parent Category")
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',store=True,recursive=True)
    sequence = fields.Integer(string="Sequence")



    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        """
            Complete name based on parent child hierarchy.
        """
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name