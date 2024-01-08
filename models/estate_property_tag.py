# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EstatePopertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag description"

    name = fields.Char(required=True)