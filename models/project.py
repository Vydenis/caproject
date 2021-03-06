# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class Project(models.Model):
    _name = 'caproject.project'
    _description = 'Projects'

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    duration = fields.Integer(string='Duration (days)', help="Duration in days")
    max_employees = fields.Integer(string='Maximum number of employees')
    # price = fields.Float(string='Price, Eur', required=True, help="Project price in Euro")


    job_ids = fields.Many2many('caproject.jobs', string="Project jobs")
    price_ids = fields.One2many('caproject.bills', 'project_id', string="Project price")


    leader_id = fields.Many2one('hr.employee', string="Team Leader", domain=[('lead', '=', True)])
    # customer_ids = fields.Many2many('res.partner', string="Customers")
    client_id = fields.Many2one('res.partner', string="Client")
    employees_ids = fields.Many2many('hr.employee', string="Employees")


    active_employees = fields.Float(string="Maximum employees", compute='_employees_in')
    employees_count = fields.Integer(
        string="Employees in project", compute='_get_employees_count', store=True)

    active = fields.Boolean(default=True, store=True)
    color = fields.Integer()
    # gali buti fields.Binary, neaisku kas geriau, bet binary tinka visiems
    # failams, ne tik paveiksleliams.
    image = fields.Image("Image", attachment=True)
    document_ids = fields.One2many('caproject.document', 'project_id', string='Documents')

    status = fields.Selection([
        ('draft', "Draft"),
        ('started', "Started"),
        ('done', "Done"),
        ('cancelled', "Cancelled"),
    ], string="Progress", default='draft', translate=True)



    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the project should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The project title must be unique"),

    ]

    # today = fields.Date(default=fields.Date.today)
    # # pabandyti padaryti, kad pasibaigus projekto laikui statusa pakeistu i neaktyvus.
    # @api.depends('today', 'end_date')
    # def _get_status(self):
    #     for r in self:
    #         if r.end_date < r.today:
    #             r.active = False


    # paskai??iuoja kiek darbo viet?? projekte u??pildyta ir per view.xml i??veda procentus ir juost??
    @api.depends('max_employees', 'employees_ids')
    def _employees_in(self):
        for r in self:
            if not r.max_employees:
                r.active_employees = 0.0
            else:
                r.active_employees = 100.0 * len(r.employees_ids) / r.max_employees

    # paskai??iuoja ir u??pildo neu??pildyta duration arba end date, jei vienas i?? j?? yra u??pildytas, o kitas ne
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1


    @api.depends('employees_ids')
    def _get_employees_count(self):
        for r in self:
            r.employees_count = len(r.employees_ids)


    # jei ??vesta daugiau darbuotoj??, nei numatytas max skai??ius i??meta ??sp??jim??, bet leid??ia i??saugoti
    @api.onchange('max_employees', 'employees_ids')
    def _verify_valid_employees(self):
        if self.max_employees < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'employees' value"),
                    'message': _("The number of active employees may not be negative"),
                },
            }
        if self.max_employees < len(self.employees_ids):
            return {
                'warning': {
                    'title': _("Too many employees in project"),
                    'message': _("Increase slots or remove excess employees"),
                },
            }

    # i??meta klaid??, jei priskirtas prie projekto lead'as yra ir tarp projekto darbuotoj??
    @api.constrains('leader_id', 'employees_ids')
    def _check_leader_not_in_employees(self):
        for r in self:
            if r.leader_id and r.leader_id in r.employees_ids:
                raise exceptions.ValidationError(_("A project leader can't be an employee in project"))


    # neleid??ia i??saugoti duomen??, jei ??vesta daugiau darbuotoj??, nei numatytas max skai??ius
    @api.constrains('max_employees', 'employees_ids')
    def _check_number_of_employees(self):
        for r in self:
            if len(r.employees_ids) > r.max_employees:
                raise exceptions.ValidationError(_("Increase slots or remove excess employees"))


    def send_project_report(self):
        # Find the e-mail template
        template = self.env.ref('caproject.caproject_project_mail_template')
        # You can also find the e-mail template like this:
        # template = self.env['ir.model.data'].get_object('send_mail_template_demo', 'example_email_template')

        # Send out the e-mail template to the user
        self.env['mail.template'].browse(template.id).send_mail(self.id)


class ProjectDocument(models.Model):
    _name = 'caproject.document'

    name = fields.Char(string='Filename')
    file = fields.Binary(string=_('File'), attachment=True)
    comment = fields.Text(string=_('Notes'))

    project_id = fields.Many2one('caproject.project')