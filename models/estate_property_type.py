# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate property type description'

    name = fields.Char(required=True)