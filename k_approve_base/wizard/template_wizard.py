# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TemplateWizard(models.TransientModel):
    _name = 'kapprove.template.wizard'
    _description = 'Template'

    templ_type = fields.Many2one('kapprove.template.type', string="Template Type", required=True)
    template = fields.Many2one('kapprove.doc.template', string="Template", required=True, domain=[('active', '=', True)])

    @api.onchange('templ_type')
    def onchange_template_type(self):
        self.template = False
        return {'domain': {'template': [('template_type', '=', self.templ_type.id)]}}

    def action_template(self):
        active_id = self.env.context.get('active_id')
        doc_id = self.env['kapprove.doc'].search([('id', '=', active_id)])

        template_id = self.template
        vals = {
            'doc_name': template_id.doc_name,
            'secret': template_id.secret,
            'priority': template_id.priority,
            'categ_id': template_id.categ_id.id,
            'detail': template_id.detail,
        }


        if template_id.tag_ids:
            vals.update({
            'tag_ids': template_id.tag_ids.ids,
            })

        if template_id.period:
            vals.update({
            'period': template_id.period.id,
            })

        approvers = []
        for rec in template_id.approver_ids:
            if rec.user_id.id not in doc_id.approver_ids.mapped('user_id').ids:
                values = {
                    'user_id': rec.user_id.id,
                    'department_id': rec.department_id.id,
                    'job_title': rec.job_title,
                    'job_position': rec.job_position.id,
                    'state': 'draft',
                    'sequence': rec.sequence,
                    'approve_type': rec.approve_type
                }
                approvers.append((0, 0, values))
        vals.update({
            'approver_ids': approvers
        })
        doc_id.write(vals)

