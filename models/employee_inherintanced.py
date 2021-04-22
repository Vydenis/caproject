# -*- coding: utf-8 -*-
from odoo import fields, models

class Partner(models.Model):
    _inherit = 'hr.employee'

    lead = fields.Boolean("Team Lead", default=False)
    project_id = fields.Many2many('caproject.project', string="Project name", readonly=True)