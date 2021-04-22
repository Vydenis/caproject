from odoo import models, fields, api


class Jobs(models.Model):
    _name = 'caproject.jobs'
    _description = 'Jobs'

    name = fields.Char(string='Title', required=True)
    project_ids = fields.Many2many('caproject.project', string="Projects")
    description = fields.Text(string='Description')
    # worker_id = fields.Many2one('hr.employee', string="Worker")