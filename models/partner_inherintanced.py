# -*- coding: utf-8 -*-
from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # instructor = fields.Boolean("Instructor", default=False)

    project_id = fields.One2many('caproject.project', 'client_id',
        string="Projects", readonly=True)