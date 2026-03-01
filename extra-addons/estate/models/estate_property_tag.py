from odoo import fields, models, api


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('estate_property_tag_check_name',
         'UNIQUE(name)', 'The tag name must be unique.')
    ]
