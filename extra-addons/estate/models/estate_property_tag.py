from odoo import fields, models, api


class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"
    _order = "name asc"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('estate_property_tag_check_name',
         'UNIQUE(name)', 'The tag name must be unique.')
    ]
