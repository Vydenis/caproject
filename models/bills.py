from odoo import models, fields, api

class Bills(models.Model):
    _name = 'caproject.bills'
    _description = 'Bills'

    name = fields.Char(string='Title', required=True)
    price = fields.Float(string='Price, Eur', required=True, help="Project price in Euro")

    project_id = fields.Many2one('caproject.project', string="Project name", required=True)

    status = fields.Selection([
        ('draft', "Draft"),
        ('sent', "Sent"),
        ('paid', "Paid"),
        ('cancelled', "Cancelled"),
    ], string="Progress", default='draft', translate=True)