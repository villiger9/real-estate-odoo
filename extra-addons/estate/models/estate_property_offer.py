from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


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
            # if the record is new, create_date is False. use today's date instead
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = start_date + \
                relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            start_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            # subtract the dates to get a 'timedelta' object, then grab the .days
            delta = offer.date_deadline - start_date
            offer.validity = delta.days
