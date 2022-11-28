# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = ('k_address1','street', 'street2', 'zip', 'city', 'state_id', 'country_id')

class kCountry(models.Model):
    _name = 'res.country'
    _inherit = 'res.country'

    name = fields.Char(string='Country Name', required=True, help='The full name of the country.')

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    name = fields.Char(index=True,translate=True)
    k_address1 = fields.Char(string='주소',translate=True)
    k_address1_eng = fields.Char(string='Address')


    country_id = fields.Many2one('res.country', string='Country',default = lambda self: self.env.company.country_id)
    country_code = fields.Char(string='국가코드', related='country_id.code',
                               default=lambda self: self.env.company.country_id.code)

    # @api.onchange('k_address1','street2')
    # def _onchange_vendor(self):
    #     if not self.street2 :
    #         self.street2 = ''
    #     self.address_all = "%s %s" % (self.k_address1 , self.street2)

    @api.model
    def create(self, vals):
        item =  super(ResPartner, self).create(vals)
        if self.env.user.lang == 'ko_KR' :
           lang = 'en_US'
        else :
           lang = 'ko_KR'

        if vals.get('k_address1_eng') :
            self.env['ir.translation'].create({
                'type': 'model',
                'name': 'res.partner,k_address1',
                'lang': lang,
                'res_id': item.id,
                'src': vals.get('k_address1'),
                'value': vals.get('k_address1_eng'),
            })
        return item

    def write(self, values):
        if self.env.user.lang == 'ko_KR' :
           lang = 'en_US'
        else :
           lang = 'ko_KR'

        if 'k_address1_eng' in values:
            item = self.env['ir.translation'].search([('type','=','model'),('lang','=',lang),('name','=','res.partner,k_address1'),('res_id','=',self.id)],limit=1)
            if item :
                _logger.warning("----write item %s", values['k_address1_eng'])
                item.update({'value':values['k_address1_eng']})
        return super(ResPartner, self).write(values)

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return list(ADDRESS_FIELDS)


    def _get_company_address_field_names(self):
        """ Return a list of fields coming from the address partner to match
        on company address fields. Fields are labeled same on both models. """
        return ['k_address1','street', 'street2', 'city', 'zip', 'state_id', 'country_id']


    def _config_kaddress(self):
        _logger.warning("----user lang %s", self.env.user.lang)
        if self.env.user.lang == "ko_KR":
            return True
        else:
            return False


    @api.model
    def _set_korea_address(self,sido,lang):
        _logger.warning("----_set_korea_address1 %s %s", sido,lang)

        country_id = self.env['res.country'].search([('code','=','KR')],limit = 1)
        if not country_id :
            country_id = self.env['res.country'].create({ 'code':'KR','name':'South Korea'})
        if  country_id :
            state_id = self.env['res.country.state'].search([('name', '=', sido),('country_id','=',country_id.id)], limit=1)
            if not state_id :
               state_id = self.env['res.country.state'].create({'name': sido,'code': sido,'country_id':country_id.id})


            return {'user_country_code':lang,'country_id':country_id.id , 'state_id':state_id.id , 'country_name' : country_id.name,'state_name' : state_id.name}
        return None


class Company(models.Model):
    _name = "res.company"
    _inherit = 'res.company'

    k_address1 = fields.Char(string='주소',translate=True)
    k_address1_eng = fields.Char(string='Address')


    country_id = fields.Many2one('res.country', string='Country',default = lambda self: self.env.company.country_id)
    country_code = fields.Char(string='국가코드', related='country_id.code',
                               default=lambda self: self.env.company.country_id.code)