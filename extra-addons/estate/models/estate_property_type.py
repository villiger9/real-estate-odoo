from odoo import fields, models, api


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties")
    sequence = fields.Integer()
    offer_ids = fields.One2many('estate.property.offer',
                                'property_type_id', string="Offers")
    offer_count = fields.Integer(
        compute="_compute_offer_count", string="Offers Count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('estate_property_type_check_name',
         'UNIQUE(name)', 'The type name must be unique.')
    ]
