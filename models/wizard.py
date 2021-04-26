# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'caproject.wizard'
    _description = "Wizard: Quick registration of emplyees to project"

    def _default_session(self):
        return self.env['caproject.project'].browse(self._context.get('active_ids'))

    project_ids = fields.Many2many('caproject.project', string="Project name", required=True, default=_default_session)
    employees_ids = fields.Many2many('hr.employee', string="Employees")

    def subscribe(self):
        for project in self.project_ids:
            project.employees_ids |= self.employees_ids
        return {}
