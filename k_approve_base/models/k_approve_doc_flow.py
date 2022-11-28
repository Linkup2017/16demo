# -*- coding: utf-8 -*-

from odoo import models, fields, api


class KApproveDocFlow(models.Model):
    _name = 'kapprove.doc.flow'
    _rec_name = 'user_id'
    _description = 'Approvers'
    _order = "sequence,id"

    @api.model
    def _default_user(self):
        """
            Function for fetching the default user
        """
        return self.env.context.get('user_id', self.env.user.id)

    user_id = fields.Many2one('res.users', string="Name", required=True)
    approve_type = fields.Selection([('sequential', 'Sequential'), ('parallel', 'Parallel')], string="Approve Type",
                            default='sequential', required=True)
    department_id = fields.Many2one('hr.department', related='user_id.employee_ids.department_id', string="Department",
                                    readonly=True)
    job_title = fields.Char(related='user_id.employee_ids.job_title', string="Job Title")
    job_position = fields.Many2one('hr.job', related='user_id.employee_ids.job_id', string="Job Position")
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'),
                              ('refused', 'Refused'), ('cancel', 'Cancel')], string="Status", default='draft', readonly=True)
    user_ids = fields.Many2many('res.users', string="Cooperation")
    doc_approver_ids = fields.Many2one('kapprove.doc', string="Approvers",ondelete='cascade')
    templ_approver_ids = fields.Many2one('kapprove.doc.template', string="Approvers")
    sequence = fields.Integer()


class KApproveTemplateDocFlow(models.Model):
    _name = 'kapprove.doc.template.flow'
    _rec_name = 'user_id'
    _description = 'Approvers'
    _order = "sequence,id"


    user_id = fields.Many2one('res.users', string="Name", required=True)
    approve_type = fields.Selection([('sequential', 'Sequential'), ('parallel', 'Parallel')], string="Approve Type",
                                    default='sequential', required=True)
    department_id = fields.Many2one('hr.department', related='user_id.employee_ids.department_id', string="Department",
                                    readonly=True)
    job_title = fields.Char(related='user_id.employee_ids.job_title', string="Job Title")
    job_position = fields.Many2one('hr.job', related='user_id.employee_ids.job_id', string="Job Position")
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'),
                              ('refused', 'Refused'), ('cancel', 'Cancel')], string="Status", default='draft', readonly=True)

    approve_doc_id = fields.Many2one('kapprove.doc', string="Approvers",ondelete='cascade',index=True)
    sequence = fields.Integer(string="Sequence")
    date = fields.Datetime(string="Date", readonly=True)


class KApproveCooperationDocFlow(models.Model):
    _name = 'kapprove.doc.share'
    _rec_name = 'user_id'
    _description = 'Cooperation'
    _order = "sequence,id"

    user_id = fields.Many2one('res.users', string="Name", required=True)
    department_id = fields.Many2one('hr.department', related='user_id.employee_ids.department_id', string="Department",
                                    readonly=True)
    job_title = fields.Char(related='user_id.employee_ids.job_title', string="Job Title")
    job_position = fields.Many2one('hr.job', related='user_id.employee_ids.job_id', string="Job Position")
    checked_date = fields.Datetime(string="Checked Date", readonly=True)
    rel_doc_cooperation_ids = fields.Many2one('kapprove.doc', string="Approvers")
    sequence = fields.Integer(string="Sequence")
    is_checked = fields.Boolean(string="Checked", readonly=True)


class KApproveFlowLine(models.Model):
    _name = 'kapprove.flow.line'
    _rec_name = 'user_id'
    _description = 'My Approver Line Approvers'

    user_id = fields.Many2one('res.users', string="Name", required=True)
    approve_type = fields.Selection([('sequential', 'Sequential'), ('parallel', 'Parallel')], string="Approve Type",
                                    default='sequential', required=True)
    department_id = fields.Many2one('hr.department', related='user_id.employee_ids.department_id', string="Department",
                                    readonly=True)
    job_title = fields.Char(related='user_id.employee_ids.job_title', string="Job Title")
    job_position = fields.Many2one('hr.job', related='user_id.employee_ids.job_id', string="Job Position")
    rel_line_approver_ids = fields.Many2one('kapprove.line', string="Approvers")

