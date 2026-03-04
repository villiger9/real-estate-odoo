from odoo import fields, models, Command
import logging
_logger = logging.getLogger(__name__)


class EstatePropertyAccount(models.Model):
    _inherit = "estate.property"

    def action_sell(self):
        print("DEBUG: The property has been sold! Preparing to create an invoice...")
        # 1. Call the original logic from the 'estate' module (sets state to 'sold')
        res = super().action_sell()

        # 2. Loop through 'self' because 'self' is a collection of records
        for record in self:
            # 3. Create the empty invoice
            self.env['account.move'].create({       # the create method doesn’t accept recordsets as field values.
                # Link to the buyer (ID only!)
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',       # Tell Odoo it's a 'Customer Invoice'
                'invoice_line_ids': [
                    # Command.create replaces (0, 0, {values})
                    Command.create({
                        'name': record.name,
                        'quantity': 1.0,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative fees',
                        'quantity': 1.0,
                        'price_unit': 100.00,
                    }),
                ],
            })
        return res
