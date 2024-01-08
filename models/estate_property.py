# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, exceptions


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate property description'

    name = fields.Char(required=True, string=u"Title")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, 
        default=lambda self: fields.datetime.now() + relativedelta(months=3), 
        string=u"Available From")
    expected_price = fields.Float(required=True,copy=False)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string=u"Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer("Total Area", compute="_compute_total_area")
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
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    active = fields.Boolean(default=True)

    STATES = [
        ('new', u'New'),
        ('offer_received', u'Offer Received'),
        ('offer_accepted', u'Offer Accepted'),
        ('sold', u'Sold'),
        ('canceled', u'Canceled'),
    ]
    state = fields.Selection(STATES, default='new')


    # State actions
    def action_sold(self):
        if self.state == "canceled":
            raise exceptions.UserError("Canceled properties cannot be sold")
        self.state = "sold"
        return True
    
    def action_cancel(self):
        if self.state == "sold":
            raise exceptions.UserError("Sold properties cannot be canceled")
        self.state = "canceled"
        return True

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "north"
        else:
            self.garden_orientation = ""

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0


    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
