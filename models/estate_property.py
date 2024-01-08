# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property description'

    name = fields.Char(required=True, string=u"Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, 
        default=lambda self: fields.datetime.now() + relativedelta(months=3), 
        string=u"Available From")
    expected_price = fields.Float(required=True, readonly=True, copy=False)
    selling_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string=u"Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north',  u'North'),
            ('south',  u'South'),
            ('east',  u'East'),
            ('west',  u'West'),
        ]
    )
    property_type_id = fields.Many2one("estate.property.type", u"Property Type")
    buyer_id = fields.Many2one("res.partner", "Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", "Salesperson", default=lambda self: self.env.uid)
    tag_ids = fields.Many2many("estate.property.tag", string=u"Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    active = fields.Boolean(default=True)

    STATES = [
        ('new', u'New'),
        ('offer_received', u'Offer Received'),
        ('offer_accepted', u'Offer Accepted'),
        ('sold', u'Sold'),
        ('canceled', u'Canceled'),
    ]
    state = fields.Selection(STATES, default='new')
