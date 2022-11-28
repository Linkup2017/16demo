# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import base64
from odoo.modules.module import get_module_resource
CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]


class KApproveTemplateType(models.Model):
    _name = 'kapprove.template.type'
    _inherit = 'mail.thread'
    _description = "Approve Template Type"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)


class KApproveTemplate(models.Model):
    _name = 'kapprove.doc.template'
    _inherit = 'mail.thread'
    _description = "Approve Template"
    _rec_name = 'doc_name'

    @api.model
    def _default_period(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('period'))

    period = fields.Many2one('kapprove.retention', string="Retention Period", domain=[('permanent', '=', True)], default=_default_period)
    secret = fields.Boolean(string="Security Approval")
    # categ_id = fields.Many2one('kapprove.category', string="Category", required=True)
    tag_ids = fields.Many2many('kapprove.doc.tag', string="Tag")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], 'Priority', default='1')
    active = fields.Boolean(string="Active", default=True)
    template_type = fields.Many2one('kapprove.template.type', string="Template Type", required=True)
    doc_name = fields.Char(string="Document Title", required=True)
    detail = fields.Html(string="Detail", sanitize_attributes=False, sanitize_form=False)

    approver_ids = fields.One2many('kapprove.doc.flow', 'templ_approver_ids', string="Approvers")

    users = fields.Many2many('res.users', compute='_compute_users')

    has_date = fields.Selection(CATEGORY_SELECTION, string="Has Date", default="no", required=True)
    has_period = fields.Selection(CATEGORY_SELECTION, string="Has Period", default="no", required=True)
    has_quantity = fields.Selection(CATEGORY_SELECTION, string="Has Quantity", default="no", required=True)
    has_amount = fields.Selection(CATEGORY_SELECTION, string="Has Amount", default="no", required=True)
    has_reference = fields.Selection(
        CATEGORY_SELECTION, string="Has Reference", default="no", required=True,
        help="An additional reference that should be specified on the request.")

    has_partner = fields.Selection(CATEGORY_SELECTION, string="Has Contact", default="no", required=True)
    has_payment_method = fields.Selection(CATEGORY_SELECTION, string="Has Payment", default="no", required=True)
    has_location = fields.Selection(CATEGORY_SELECTION, string="Has Location", default="no", required=True)
    has_product = fields.Selection(
        CATEGORY_SELECTION, string="Has Product", default="no", required=True,
        help="Additional products that should be specified on the request.")
    has_partners = fields.Selection(
        CATEGORY_SELECTION, string="Has Partners", default="no", required=True,
        help="Additional products that should be specified on the request.")
    has_description = fields.Selection(CATEGORY_SELECTION, string="Has Description", default="no", required=True)
    has_totalamount = fields.Selection(CATEGORY_SELECTION, string="Has amount", default="no", required=True)
    has_purpose = fields.Selection(CATEGORY_SELECTION, string="Has purpose", default="no", required=True)

    number_has_partner = fields.Integer(string="", default="1")
    number_has_date = fields.Integer(string="", default="1")
    number_has_period = fields.Integer(string="", default="1")
    number_has_product = fields.Integer(string="", default="1")
    number_has_quantity = fields.Integer(string="", default="1")
    number_has_amount = fields.Integer(string="", default="1")
    number_has_reference = fields.Integer(string="", default="1")
    number_has_payment_method = fields.Integer(string="", default="1")
    number_has_location = fields.Integer(string="", default="1")
    number_has_partners = fields.Integer(string="", default="1")
    number_has_description = fields.Integer(string="", default="1")
    number_has_totalamount = fields.Integer(string="", default="1")
    number_has_purpose = fields.Integer(string="", default="1")


    str_has_partner = fields.Char(string="" , translate=True)
    str_has_date = fields.Char(string="" , translate=True)
    str_has_period = fields.Char(string="" , translate=True)
    str_has_product = fields.Char(string="" , translate=True)
    str_has_quantity = fields.Char(string="" , translate=True)
    str_has_amount = fields.Char(string="" , translate=True)
    str_has_reference = fields.Char(string="" , translate=True)
    str_has_payment_method = fields.Char(string="" , translate=True)
    str_has_location = fields.Char(string="" , translate=True)
    str_has_partners = fields.Char(string="", translate=True)
    str_has_description = fields.Char(string="", translate=True)
    str_has_totalamount = fields.Char(string="", translate=True)
    str_has_purpose = fields.Char(string="", translate=True)

    side_has_partner = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_date = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_period = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_reference = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right'),
        ('row', 'Row')], string="Left or Right", default="left", required=True)
    side_has_payment_method = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_location = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_partners = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right'),
        ('row', 'Row')], string="Left or Right", default="left", required=True)
    side_has_description = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_totalamount = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_product = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_quantity = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_amount = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)
    side_has_purpose = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="Left or Right", default="left", required=True)

    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)

    def _get_default_image(self):
        default_image_path = get_module_resource('k_approve_base', 'static/src/img', 'clipboard-check-solid.svg')
        return base64.b64encode(open(default_image_path, 'rb').read())

    image = fields.Binary(string='Image', default=_get_default_image)


    @api.depends('approver_ids')
    def _compute_users(self):
        if self.approver_ids:
            users_ids = self.approver_ids.mapped('user_id')
            self.users += users_ids
        else:
            self.users = None

    @api.model
    def create(self, values):
        res = super(KApproveTemplate, self).create(values)
        if res.approver_ids:
            last_approver = self.env['kapprove.doc.flow'].search([('id', '=', max(res.approver_ids.ids))])
            if last_approver.approve_type != 'sequential':
                raise UserError(_("Please specify the approve type for the final approver as 'Sequential'"))
        return res

    def write(self, values):
        res = super(KApproveTemplate, self).write(values)
        if self.approver_ids:
            last_approver = self.env['kapprove.doc.flow'].search([('id', '=', max(self.approver_ids.ids))])
            if last_approver.approve_type != 'sequential':
                raise UserError(_("Please specify the approve type for the final approver as 'Sequential'"))
        return res

    def create_document(self):
        self.ensure_one()
        # 'id_k_approval_doc_form_view'
        view_id = self.env.ref('k_approve_base.id_k_approval_doc_form_view').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "kapprove.doc",
            "views": [[view_id, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'default_name': self.doc_name,
                'default_doc_name': self.doc_name,
                'default_template_id': self.id,
                'default_bigo':self.detail,
                'default_tag_ids': self.tag_ids.ids,
            },
        }


