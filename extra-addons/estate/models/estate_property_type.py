from odoo import fields, models, api


class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('estate_property_type_check_name',
         'UNIQUE(name)', 'The type name must be unique.')
    ]
