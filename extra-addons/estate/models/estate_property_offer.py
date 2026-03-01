from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils  # Import the Odoo helper
from odoo.exceptions import UserError


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
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for offer in self:
            # Fallback: if record isn't saved yet, use today's date
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = base_date + \
                relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            base_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            # Calculate the difference between the set deadline and the start date
            offer.validity = (offer.date_deadline - base_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['offer_accepted', 'sold', 'cancelled']:
                raise UserError("can't accept offer!")

            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
