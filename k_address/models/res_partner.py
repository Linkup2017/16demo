# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from lxml import etree

from odoo import api, models, fields
from odoo.tools.translate import _


import logging
#Get the logger
_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    country_enforce_cities = fields.Boolean(related='country_id.enforce_cities', readonly=True)
    city_id = fields.Many2one('res.city', string='City of Address',domain="[('state_id', '=', state_id)]" )



    @api.onchange('state_id')
    def _onchange_state(self):
        if self.state_id and self.state_id != self.city_id.state_id:
            self.city_id = False

    @api.onchange('city_id')
    def _onchange_city_id(self):
        _logger.warning('---- _onchange_city_id (%s)',self.city_id.name)
        if self.city_id:
            self.city = self.city_id.name
            self.zip = self.city_id.zipcode

    @api.model
    def _fields_view_get_address(self, arch):
        arch = super(Partner, self)._fields_view_get_address(arch)
        # render the partner address accordingly to address_view_id
        _logger.warning('---- _fields_view_get_address (%s)',arch)
        doc = etree.fromstring(arch)
        _logger.warning('---- doc (%s)',doc)

        if doc.xpath("//field[@name='city_id']"):
            return arch

        replacement_xml = """
            <div>
                <field name="country_enforce_cities" invisible="1"/>
                <field name="parent_id" invisible="1"/>
                <field name='city' placeholder="%(placeholder)s" class="o_address_city"
                    attrs="{
                        'invisible': [('country_enforce_cities', '=', True)],
                        'readonly': [('type', '=', 'contact')%(parent_condition)s]
                    }"
                />
                <field name='city_id' placeholder="%(placeholder)s" string="%(placeholder)s" class="o_address_city"
                    context="{'default_country_id': country_id,
                              'default_name': city,
                              'default_zipcode': zip,
                              'default_state_id': state_id}"
                    domain="[('state_id', '=', state_id)]"
                    attrs="{
                        'invisible': [('country_enforce_cities', '=', False)],
                        'readonly': [('type', '=', 'contact')%(parent_condition)s]
                    }"
                />
            </div>
        """

        replacement_data = {
            'placeholder': _('City'),
        }

        def _arch_location(node):
            in_subview = False
            view_type = False
            parent = node.getparent()

            _logger.warning('---- parent (%s)',parent)

            while parent is not None and (not view_type or not in_subview):
                if parent.tag == 'field':
                    in_subview = True
                elif parent.tag in ['list', 'tree', 'kanban', 'form']:
                    view_type = parent.tag
                parent = parent.getparent()
            return {
                'view_type': view_type,
                'in_subview': in_subview,
            }

        for city_node in doc.xpath("//field[@name='city']"):
            location = _arch_location(city_node)
            _logger.warning('---- location (%s)',location)
            replacement_data['parent_condition'] = ''
            if location['view_type'] == 'form' or not location['in_subview']:
                replacement_data['parent_condition'] = ", ('parent_id', '!=', False)"

            replacement_formatted = replacement_xml % replacement_data
            _logger.warning('---- replacement_formatted (%s)',replacement_formatted)
            for replace_node in etree.fromstring(replacement_formatted).getchildren():
                _logger.warning('---- replace_node (%s)',replace_node)
                city_node.addprevious(replace_node)

            parent = city_node.getparent()
            _logger.warning('---- parent (%s)',parent)

            parent.remove(city_node)

        arch = etree.tostring(doc, encoding='unicode')
        return arch
