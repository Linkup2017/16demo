# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
_logger = logging.getLogger(__name__)
import json

class KApproveDocnode(models.Model):
    _name = 'kapprove.doc.node'
    _description = "Approval Document left node"

    doc_id = fields.Many2one('kapprove.doc','Document')
    doc_left_name = fields.Char(string="Title")
    doc_left_contents = fields.Char(string="Contents")
    doc_right_name = fields.Char(string="Title")
    doc_right_contents = fields.Char(string="Contents")


class WizardEmployeeInformationExcelReport(models.TransientModel):
    _name = 'wizard.emp.info.excel.report'

    name = fields.Char('File Name', size=64)
    report = fields.Binary('Prepared File', filters='.html', readonly=True)

class KApproveDoc(models.Model):
    _name = 'kapprove.doc'
    _inherit = ['mail.thread']
    _description = "Approval Document"
    _rec_name = 'name'


    @api.model
    def _default_user(self):
        """
            Function for fetching the default user
        """
        return self.env.context.get('user_id', self.env.user.id)

    users = fields.Many2many('res.users', compute='_compute_users')
    cooperation_users = fields.Many2many('res.users', compute='_compute_cooperation_users')

    @api.depends('cooperation_ids')
    def _compute_cooperation_users(self):
        if self.cooperation_ids:
            user_id = self._default_user()
            users_ids = self.cooperation_ids.mapped('user_id')
            filtered_user_ids = users_ids.filtered(lambda l: l.id != user_id)

            self.cooperation_users += filtered_user_ids
        else:
            self.cooperation_users = None

    @api.depends('approver_ids')
    def _compute_users(self):
        if self.approver_ids:
            user_id = self._default_user()
            users_ids = self.approver_ids.mapped('user_id')
            filtered_user_ids = users_ids.filtered(lambda l: l.id != user_id)

            self.users += filtered_user_ids
        else:
            self.users = None

    @api.model
    def _default_period(self):
        return int(self.env['ir.config_parameter'].sudo().get_param('period'))


    def _compute_approve_button_visibility(self):
        self._compute_approval_user_id()
        for rec in self:
            current_user = self._default_user()
            if current_user in rec.submit_user_id.ids:
                rec.current_approver = True
            else:
                rec.current_approver = False


    approver_line_ids = fields.One2many('kapprove.doc.line','approve_doc_id',string="Approver Lines")
    current_approver = fields.Boolean(string="Current Approver", compute=_compute_approve_button_visibility)

    name = fields.Char(string="Name", default='New', readonly=True, copy=False)
    doc_name = fields.Char(string="Document Title")
    period = fields.Many2one('kapprove.retention', string="Retention Period",domain=[('permanent', '=', True)], default=_default_period)
    secret = fields.Boolean(string="Security Approval")
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], 'Priority', default='1')
    user_id = fields.Many2one('res.users', readonly=True, string="Created By", required=True, default=_default_user)
    create_on = fields.Datetime(string="Creation On", default=fields.Datetime.now, required=True, readonly=True)
    # categ_id = fields.Many2one('kapprove.category', string="Category")
    tag_ids = fields.Many2many('kapprove.doc.tag', string="Tags", readonly=True)
    origin = fields.Char(string="Source Document")
    detail = fields.Char(string="Detail")
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('in_progress', 'In progress'),
        ('approved', 'Approved'),
        ('refused', "Refused"),
        ('cancel', 'Cancel')
    ], 'State', default='draft', tracking=True)
    approver_ids = fields.One2many('kapprove.doc.template.flow', 'approve_doc_id', string="Approvers",copy = True)
    cooperation_ids = fields.One2many('kapprove.doc.share', 'rel_doc_cooperation_ids', string="Cooperation")
    user_ids = fields.Many2many('res.users', string="Cooperation")
    approval_state = fields.Selection([('to_approval', 'To approval'),('approved', 'Approved')],string = 'Approval State')
    partner_ids = fields.Many2many('res.partner', string="Partners")
    template_id = fields.Many2one('kapprove.doc.template', string="Template", required=True)
    product_line_ids = fields.One2many('kapproval.product.line', 'approval_request_id',copy = True)
    company_id = fields.Many2one(
        string='Company', related='template_id.company_id',
        store=True, readonly=True, index=True)


    has_date = fields.Selection(related="template_id.has_date")
    has_period = fields.Selection(related="template_id.has_period")
    has_quantity = fields.Selection(related="template_id.has_quantity")
    has_amount = fields.Selection(related="template_id.has_amount")
    has_reference = fields.Selection(related="template_id.has_reference")
    has_partner = fields.Selection(related="template_id.has_partner")
    has_payment_method = fields.Selection(related="template_id.has_payment_method")
    has_location = fields.Selection(related="template_id.has_location")
    has_product = fields.Selection(related="template_id.has_product")
    has_partners = fields.Selection(related="template_id.has_partners")
    has_description = fields.Selection(related="template_id.has_partners")
    has_totalamount = fields.Selection(related="template_id.has_totalamount")
    has_purpose = fields.Selection(related="template_id.has_purpose")

    number_has_partner = fields.Integer(string="has_partner", related="template_id.number_has_partner")
    number_has_date = fields.Integer(string="has_date", related="template_id.number_has_date")
    number_has_period = fields.Integer(string="has_period", related="template_id.number_has_period")
    number_has_product = fields.Integer(string="has_product", related="template_id.number_has_product")
    number_has_quantity = fields.Integer(string="has_quantity", related="template_id.number_has_quantity")
    number_has_amount = fields.Integer(string="has_amount", related="template_id.number_has_amount")
    number_has_reference = fields.Integer(string="has_reference", related="template_id.number_has_reference")
    number_has_payment_method = fields.Integer(string="has_payment_method",
                                               related="template_id.number_has_payment_method")
    number_has_location = fields.Integer(string="has_location", related="template_id.number_has_location")
    number_has_partners = fields.Integer(string="has_location", related="template_id.number_has_partners")
    number_has_description = fields.Integer(string="has_location", related="template_id.number_has_description")
    number_has_totalamount = fields.Integer(string="has_totalamount", related="template_id.number_has_totalamount")
    number_has_purpose = fields.Integer(string="has_purpose", related="template_id.number_has_purpose")

    str_has_partner = fields.Char(string="has_partner", related="template_id.str_has_partner")
    str_has_date = fields.Char(string="has_date", related="template_id.str_has_date")
    str_has_period = fields.Char(string="has_period", related="template_id.str_has_period")
    str_has_product = fields.Char(string="has_product", related="template_id.str_has_product")
    str_has_quantity = fields.Char(string="has_quantity", related="template_id.str_has_quantity")
    str_has_amount = fields.Char(string="has_amount", related="template_id.str_has_amount")
    str_has_reference = fields.Char(string="has_reference", related="template_id.str_has_reference")
    str_has_payment_method = fields.Char(string="has_payment_method",
                                         related="template_id.str_has_payment_method")
    str_has_location = fields.Char(string="has_location", related="template_id.str_has_location")
    str_has_partners = fields.Char(string="has_partners", related="template_id.str_has_partners")
    str_has_description = fields.Char(string="has_partners", related="template_id.str_has_description")
    str_has_totalamount = fields.Char(string="has_totalamount", related="template_id.str_has_totalamount")
    str_has_purpose = fields.Char(string="has_purpose", related="template_id.str_has_purpose")

    side_has_partner = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_partner", related="template_id.side_has_partner")
    side_has_date = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_date", related="template_id.side_has_date")
    side_has_period = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_period", related="template_id.side_has_period")
    side_has_product = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_product", related="template_id.side_has_product")
    side_has_quantity = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_quantity", related="template_id.side_has_quantity")
    side_has_amount = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_amount", related="template_id.side_has_amount")
    side_has_reference = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_reference", related="template_id.side_has_reference")
    side_has_payment_method = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_payment_method",
                                         related="template_id.side_has_payment_method")
    side_has_location = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_location", related="template_id.side_has_location")
    side_has_partners = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_partners", related="template_id.side_has_partners")
    side_has_description = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_partners", related="template_id.side_has_description")
    side_has_totalamount = fields.Selection([
                ('left', 'Left'),
                ('right', 'Right')], string="has_totalamount", related="template_id.side_has_totalamount")
    side_has_purpose = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')], string="has_purpose", related="template_id.side_has_purpose")


    date = fields.Datetime(string="Date")
    date_start = fields.Datetime(string="Date start")
    date_end = fields.Datetime(string="Date end")
    quantity = fields.Float(string="Quantity")
    location = fields.Char(string="Location")
    date_confirmed = fields.Datetime(string="Date Confirmed")
    partner_id = fields.Many2one('res.partner', string="Contact", check_company=True)
    reference = fields.Char(string="Reference")
    amount = fields.Float(string="Amount")
    description = fields.Char(string="Description")
    currency_id = fields.Many2one('res.currency', compute='_get_company_currency', readonly=True)
    totalamount = fields.Monetary(currency_field='currency_id' , string="Amount")
    purpose = fields.Char(string="purpose")
    bigo = fields.Html(string="Bigo",sanitize_attributes=False, sanitize_form=False)
    nodes = fields.One2many('kapprove.doc.node','doc_id' ,compute='_get_nodes', readonly=True)
    nodes_cnt = fields.Integer('Node count',default = 4)

    def _set_array_make_value(self,leftnodes,rightnodes,has_1,num_1,side_1,str_1,value):
        if has_1 != 'no':
            if side_1 == 'left':
                leftnodes.append(
                    {
                        "seq": num_1,
                        "side": side_1,
                        "header": str_1,
                        "string": value,
                    }
                )
            else:
                rightnodes.append(
                    {
                        "seq": num_1,
                        "side": side_1,
                        "header": str_1,
                        "string": value,
                    }
                )


    def _get_nodes(self):
        leftnodes = []
        rightnodes = []
        for doc in self:
            if doc.has_date != 'no'  and doc.date:
               value =  doc.date.strftime("%Y-%m-%d")
               self._set_array_make_value(leftnodes,rightnodes,doc.has_date,doc.number_has_date,
                                          doc.side_has_date,doc.str_has_date,value)
            if doc.has_period != 'no':
               value = doc.date_start.strftime("%Y-%m-%d") + '~' + doc.date_end.strftime("%Y-%m-%d")
               self._set_array_make_value(leftnodes,rightnodes,doc.has_period,doc.number_has_period,
                                          doc.side_has_period,doc.str_has_period,value)
            if doc.has_partner != 'no' and doc.partner_id:
               value =  doc.partner_id.name
               self._set_array_make_value(leftnodes,rightnodes,doc.has_partner,doc.number_has_partner,
                                          doc.side_has_partner,doc.str_has_partner,value)

            if doc.has_location != 'no' :
                value = doc.location
                self._set_array_make_value(leftnodes, rightnodes, doc.has_location, doc.number_has_location,
                                           doc.side_has_location, doc.str_has_location, value)

            if doc.has_partners != 'no' :
                value = '이진용,이지은'
                self._set_array_make_value(leftnodes, rightnodes, doc.has_partners, doc.number_has_partners,
                                           doc.side_has_partners, doc.str_has_partners, value)
            if doc.has_totalamount != 'no' :
                value = str(doc.totalamount) + "원"
                self._set_array_make_value(leftnodes, rightnodes, doc.has_totalamount, doc.number_has_totalamount,
                                           doc.side_has_totalamount, doc.str_has_totalamount, value)
            if doc.has_reference != 'no' :
                value = doc.reference
                self._set_array_make_value(leftnodes, rightnodes, doc.has_reference, doc.number_has_reference,
                                           doc.side_has_reference, doc.str_has_reference, value)
            if doc.has_purpose != 'no' :
                value = doc.purpose
                self._set_array_make_value(leftnodes, rightnodes, doc.has_purpose, doc.number_has_purpose,
                                           doc.side_has_purpose, doc.str_has_purpose, value)

            leftnodes = sorted(leftnodes, key = lambda k: k['seq'])
            rightnodes = sorted(rightnodes, key=lambda k: k['seq'])

            doc.nodes.unlink()
            len_left = len(leftnodes)
            len_right = len(rightnodes)
            len_max = len_left
            if len_left < len_right:
                len_max = len_right

            for cnt in range(len_max):
                left_name = ''
                left_contents = ''
                right_name = ''
                right_contents = ''
                if cnt < len_left :
                    left_name = leftnodes[cnt]['header']
                    left_contents = leftnodes[cnt]['string']
                if cnt < len_right:
                    right_name = rightnodes[cnt]['header']
                    right_contents = rightnodes[cnt]['string']

                doc.update({
                    'nodes':
                    [(0, 0, {
                        'doc_left_name': left_name,
                        'doc_left_contents': left_contents,
                        'doc_right_name': right_name,
                        'doc_right_contents': right_contents
                    })]
                })


    def _get_company_currency(self):
        for doc in self:
            if doc.company_id:
                doc.currency_id = doc.sudo().company_id.currency_id
            else:
                doc.currency_id = self.env.company.currency_id

    @api.depends('approver_ids.state','approver_ids.approve_type', 'approver_ids.user_id', 'state', 'current_approver')
    def _compute_approval_user_id(self):
        _logger.warning('--__compute_approval_user_id')
        params = self.env['ir.config_parameter'].sudo()
        is_sequential = params.get_param('k_approve_base.is_sequential')
        for rec in self:
            rec.submit_user_id = None
            if rec.approver_ids and rec.state not in ['draft']:
                approvers = rec.approver_ids.filtered(lambda l: l.state == 'to_approve').sorted(
                    lambda l: l.sequence
                )
                check = 0
                for approver in approvers:
                    _logger.warning('---approver %s %s', approver.approve_type, approver.user_id.name)
                    if is_sequential == False:
                        if approver.approve_type == 'sequential' and check == 0:
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            break
                        elif approver.approve_type == 'sequential' and check == 1:
                            break
                        elif approver.approve_type == 'parallel':
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            check = 1
                    else:
                        if approver.approve_type == 'sequential' and check == 0:
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            break
                        elif approver.approve_type == 'sequential' and check == 1:
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            break
                        elif approver.approve_type == 'parallel':
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            check = 1

                # rec._compute_approve_button_visibility()


    submit_user_id = fields.Many2many('res.users', 'approve_doc_rel', string="Submit User", compute=_compute_approval_user_id, store=True)
    doc_type = fields.Char(string="Document Type")

    checked_state = fields.Selection([('to_checked', 'To checked'), ('checked', 'Checked')],
                                     string='Checked State')
    mine_state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('in_progress', 'In progress'),
        ('approved', 'Approved'),
        ('refused', "Refused"),
        ('cancel', 'Cancel')
    ], 'My document')

    @api.depends('user_ids')
    def _compute_cooperation_user_id(self):
        for rec in self:
            if rec.user_ids:
                rec.cooperation_user_ids = [(6, 0, rec.user_ids.ids)]
            else:
                rec.cooperation_user_ids = None

    cooperation_user_ids = fields.Many2many('res.users', 'cooperation_user_rel', string="Coperation User", compute=_compute_cooperation_user_id, store=True)
    def _compute_current_user(self):
        current_user_id = self._default_user()
        for rec in self:
            if rec.user_id.id == current_user_id:
                rec.current_user = True
            else:
                rec.current_user = False

    current_user = fields.Boolean(string="Current User", compute=_compute_current_user)

    @api.depends('approver_ids')
    def _compute_approved_doc(self):
        for rec in self:
            approvers = rec.approver_ids.search([('state', 'not in', ['approved', 'refused', 'cancel'])], limit=1)
            rec.is_approved = False

    is_approved = fields.Boolean(string="Is Approved", compute=_compute_approved_doc)
    is_refused = fields.Boolean(string="Is Refused")
    is_cancelled = fields.Boolean(string="Is Cancelled")

    @api.depends('approver_ids')
    def _compute_my_approval(self):
        for rec in self:
            if rec.state != 'draft':
                if rec.approver_ids:
                    user_ids = rec.approver_ids.mapped('user_id')
                    if self.env.user.id in user_ids.ids:
                        rec.is_my_approval = True
                    else:
                        rec.is_my_approval = False
                else:
                    rec.is_my_approval = False
            else:
                rec.is_my_approval = False

    is_my_approval = fields.Boolean(string="Is My Approval", store=True, compute=_compute_my_approval)
    submit_date = fields.Datetime(string="Submitted Date", readonly=True)
    approve_date = fields.Date(string="Approved Date", readonly=True)

    def action_submit(self):
        if not self.name or not self.period :
            raise UserError("Please enter 'Document Title', 'Retention Period' and 'Category'")

        if self.approver_ids:
            for rec in self.approver_ids:
                rec.write({
                    'state': 'to_approve'
                })
            self.write({
                'state': 'submit',
                'submit_date': datetime.now()
            })
        if not self.approver_ids:
            message_id = self.env['approver.select.wizard'].create({
                'message': "The approver is not set, If you submit,"
                           " this will be approved immediately. Do you want to proceed?"})
            return {
                'name': 'Warning',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'approver.select.wizard',
                'res_id': message_id.id,
                'target': 'new'
            }
        self._compute_approval_process()


    def action_template(self):
        return {
            'name': "Template",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'kapprove.template.wizard',
            'target': 'new'
        }


    def action_refuse(self):
        return {
            'name': "Refuse Approval",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'kapprove.refuse.wizard',
            'target': 'new',
            'context': {
                'default_secret': self.secret,
            }
        }


    def action_cancel(self):
        self.write({
            'state': 'cancel'
        })
        self._compute_approval_process()

    def action_archive_document(self):
        documents = self.env['kapprove.doc'].search([])
        for rec in documents:
            if rec.period:
                create_date = rec.create_on.date()
                tot_period = rec.period.period
                if rec.period.date_period == 'days':
                    archive_date = create_date + timedelta(days=tot_period)
                elif rec.period.date_period == 'months':
                    archive_date = create_date + relativedelta(months=tot_period)
                else:
                    archive_date = create_date + relativedelta(years=tot_period)
                if archive_date == datetime.today().date():
                    rec.active = False


    def action_approve(self):
        if self.secret:
            return {
                'name': "Security Approval",
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'kapprove.security.wizard',
                'target': 'new',
            }
        if self.approver_ids:
            if self.env.user.id in self.approver_ids.mapped('user_id').ids:
                approver_id = self.approver_ids.filtered(lambda l:l.user_id.id == self.env.user.id)
                approver_id.write({
                    'state': 'approved',
                    'date': datetime.now()
                })
                self.message_post(body="Approval Done")

            approve_status = self.approver_ids.filtered(lambda l:l.state not in ['approved'])
            last_approver = self.env['kapprove.doc.template.flow'].search([('id', '=', max(self.approver_ids.ids))])
            if last_approver.state == 'approved':
                self.write({
                        'state': 'approved',
                        'approve_date': datetime.now().date()
                    })
            else:
                self.write({
                    'state': 'in_progress'
                })
        self._compute_approval_process()
        return {
            'name': "Approve",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'approval.wizard',
            'target': 'new',
        }

        # self.write({
        #     'state': 'approved'
        # })

    @api.depends('cooperation_ids.user_id', 'user_id', 'cooperation_ids.is_checked', 'user_ids')
    def _compute_doc_check(self):
        user_id = self._default_user()
        for rec in self:
            cooperation_users = rec.user_ids

            check_user = rec.cooperation_ids.filtered(lambda l: l.user_id.id == user_id)
            if user_id in cooperation_users.ids:
                rec.doc_check = False
                if check_user.is_checked == True:
                    rec.doc_check = True
                else:
                    rec.doc_check = False
            else:
                rec.doc_check = True
    doc_check = fields.Boolean(string="Doc Check", compute=_compute_doc_check)

    @api.model
    def create(self, values):
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'kapprove.doc') or 'New'


        res = super(KApproveDoc, self).create(values)

        value = {'approve_doc_id': res.id, 'approver_id': res.user_id.id,'mine_state': 'draft'}
        docnode = self.env['kapprove.doc.line'].create(value)
        _logger.warning('---create line %s', value)

        if res.approver_ids:
            last_approver = self.env['kapprove.doc.template.flow'].search([('id', '=', max(res.approver_ids.ids))])
            if last_approver.approve_type != 'sequential':
                raise UserError(_("Please specify the approve type for the final approver as 'Sequential'"))
        return res

    @api.model
    def new_view(self):
        _logger.warning('--__new_view')
        return {
            "type": "ir.actions.act_window",
            "res_model": "kapprove.doc.template",
            "views": [[False, "kanban"]],
            "search_view_id":[self.env.ref('k_approve_base.search_approve_type').id, 'search'],
            "context": {"search_default_group_by_template": 1},

        }

    def write(self, values):
        res = super(KApproveDoc, self).write(values)
        if self.approver_ids:
            last_approver = self.env['kapprove.doc.template.flow'].search([('id', '=', max(self.approver_ids.ids))])
            if last_approver.approve_type != 'sequential':
                raise UserError(_("Please specify the approve type for the final approver as 'Sequential'"))
        # return {'domain': {'my_approver_line_id': [('user_id', '=', self._default_user())]}}

        return res

    def toggle_active(self):
        res = super(KApproveDoc, self).toggle_active()
        if not self.env.user.has_group('k_approve_base.kapproval_group_manager'):
            raise UserError("You don't have the Access to Archive this Document")
        return res


    def action_check(self):
        user_id = self._default_user()
        check_user = self.cooperation_ids.filtered(lambda l: l.user_id.id == user_id)
        check_user.is_checked = True
        self.write({'doc_check': True})
        check_user.checked_date = datetime.now()
        if user_id in self.cooperation_user_ids.ids:
            if check_user.is_checked == True:
                self.write({'cooperation_user_ids': [(3, user_id)]})
                self._compute_approval_process()



    @api.onchange('user_ids')
    def onchange_user_ids(self):
        users = []
        print("xxxxxxxx", self.user_ids)
        existing_users = self.cooperation_ids.mapped('user_id')
        for rec in self.user_ids:
            user_id = self.env['res.users'].search([('id', '=', rec.ids[0])])
            print("YYYYYYY", user_id)
            if user_id.id not in existing_users.ids:
                values = {
                    'user_id': user_id.id
                }
                users.append((0, 0, values))
                print(users)
        self.cooperation_ids = users

    # @api.model
    # def search_panel_select_range(self, field_name, **kwargs):
    #     _logger.warning('--**search_panel_select_range %s',field_name)
    #
    #     if field_name == "mine_state" or field_name == "approval_state" or field_name == "checked_state":
    #         _logger.warning(field_name)
    #         docs = self.env['kapprove.doc'].search([])
    #         for doc in docs:
    #             doc._compute_approval_process()
    #
    #     res = super(KApproveDoc, self).search_panel_select_range(field_name, **kwargs)
    #     return res

    my_approver_line_id = fields.Many2one('kapprove.line', string="My Approver Line",
                                          domain="[('user_id', '=', user_id)]")

    @api.onchange('my_approver_line_id')
    def onchange_my_approver_line_id(self):
        approvers = []
        for rec in self.my_approver_line_id.approver_ids:
            values = {
                'user_id': rec.user_id.id,
                'department_id': rec.department_id.id,
                'job_title': rec.job_title,
                'job_position': rec.job_position.id,
                'state': 'draft',
                'approve_type': rec.approve_type
            }
            approvers.append((0, 0, values))
        self.approver_ids = None
        self.user_ids = None
        self.cooperation_ids = None
        self.approver_ids = approvers
        self.user_ids = self.my_approver_line_id.cooperation_user_ids

    def action_recompute_submit_userid(self):
        for doc in self:
            doc._compute_approval_user_id()

    def _compute_approval_line_user_id(self):
        _logger.warning('--__compute_approval_line_user_id')
        params = self.env['ir.config_parameter'].sudo()
        is_sequential = params.get_param('k_approve_base.is_sequential')
        for rec in self:
            rec.submit_user_id = None
            if rec.approver_ids and rec.state not in ['draft']:
                approvers = rec.approver_ids.filtered(lambda l: l.state == 'to_approve').sorted(
                    lambda l: l.sequence
                )
                check = 0
                for approver in approvers:
                    _logger.warning('---approver %s %s', approver.approve_type, approver.user_id.name)
                    if is_sequential == False:
                        if approver.approve_type == 'sequential' and check == 0:
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            break
                        elif approver.approve_type == 'sequential' and check == 1:
                            break
                        elif approver.approve_type == 'parallel':
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            check = 1
                    else:
                        if approver.approve_type == 'sequential' and check == 0:
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            break
                        elif approver.approve_type == 'sequential' and check == 1:
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            break
                        elif approver.approve_type == 'parallel':
                            rec.submit_user_id = [(4, approver.user_id.id)]
                            check = 1

                # rec._compute_approve_button_visibility()

    def _compute_approval_process(self):
        # 결재자 찾기
        self._compute_approval_user_id()
        _logger.warning('--->_compute_approval_process %s %s %s', self.id,self.approver_ids.user_id,self.submit_user_id)

        for suser in self.approver_ids :
            docnode = self.env['kapprove.doc.line'].search([('approve_doc_id', '=', self.id),('approver_id','=',suser.user_id.id)])

            if len(docnode) == 0:
                value = {'approve_doc_id':self.id,'approver_id' :suser.user_id.id }
                docnode = self.env['kapprove.doc.line'].create(value)
                _logger.warning('---create line %s',value)

            if suser.user_id.id in self.submit_user_id.ids :
                docnode.write({'approval_state': 'to_approval'})
            if suser.state == 'approved' :
                docnode.write({'approval_state': 'approved'})

            _logger.warning(docnode)


        docnode = self.env['kapprove.doc.line'].search(
            [('approve_doc_id', '=', self.id), ('approver_id', '=', self.user_id.id)])
        if len(docnode) == 0:
            mine_state = self.state
            value = {'approve_doc_id': self.id,'approver_id' :self.user_id.id, 'mine_state': mine_state}
            docnode = self.env['kapprove.doc.line'].create(value)
            _logger.warning('---create line %s', value)
        else :
            docnode.update({'mine_state':self.state})

        if self.user_id.id in self.submit_user_id.ids:
            docnode.write({'approval_state': 'to_approval'})


        for suser in self.approver_ids:
            docnode = self.env['kapprove.doc.line'].search(
                [('approve_doc_id', '=', self.id), ('approver_id', '=', suser.user_id.id)])
            if suser.user_id.id in self.user_ids.ids:
                if docnode.approval_state == 'approved' and self.doc_check == False:
                    docnode.write({'checked_state': 'to_checked'})
                elif docnode.approval_state == 'approved' and self.doc_check == True:
                    docnode.write({'checked_state': 'checked'})
            else:
                docnode.write({'checked_state': None})

            # docnode.set_panel_select_range()

        # self.env['base'].search_panel_select_range('approval_state')
        # self.env['base'].search_panel_select_range('checked_state')
        # self.env['base'].search_panel_select_range('mine_state')

