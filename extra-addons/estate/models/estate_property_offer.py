from typing import Required
from odoo import fields, models, api


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(string='Status',
                              selection=[('accepted', 'Accepted'),
                                         ('refused', 'Refused')],
                              copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
