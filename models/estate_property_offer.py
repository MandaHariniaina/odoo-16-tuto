# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer description"

    price = fields.Float()
    state = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity(Days)",default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    def action_refuse(self):
        self.state = "refused"
        return True

    def action_accept(self):
        # Refuse all property previously accepted offer
        for accepted_offer in self.env["estate.property.offer"].search([("property_id", "=", self.property_id.id), ("state", "=", "accepted")]):
            accepted_offer.state = "refused"
        self.state = "accepted"
        self.property_id.selling_price = self.price
        return True

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

