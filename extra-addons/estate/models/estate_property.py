from odoo import _, fields, models, api
from odoo.tools import date_utils  # Import the Odoo helper
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class estateProperty(models.Model):
    _name = "estate.property"       # attribute
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: date_utils.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),
                   ('east', 'East'), ('west', 'West')],
    )
    active = fields.Boolean(default=True)

    state = fields.Selection(string='State',
                             selection=[('new', 'New'),
                                        ('offer_received', 'Offer Received'),
                                        ('offer_accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('cancelled', 'Cancelled')],
                             required=True,
                             default='new')
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for a in self:
            a.total_area = a.living_area + a.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            # use mapped() to get a list of prices, then max() to find the highest
            # provide [0] as a default in case there are no offers yet
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
            return {'warning': {
                'title': _("Warning"),
                'message': ('This will reset orientation and area to 0')}}

    def action_sell(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("can't sell a cancelled property!")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("can't cancel a sold property!")
            record.state = "cancelled"
        return True
