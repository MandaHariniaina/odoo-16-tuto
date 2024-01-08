# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer description"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

