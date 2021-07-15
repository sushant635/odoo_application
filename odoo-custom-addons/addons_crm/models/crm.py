from odoo import  api,fields, models

class YearMaster(models.Model):
    _name="year.master"

    name =fields.Char('Year')
    start_date = fields.Date('Start Date')
    enn_date = fields.Date('End Date')
    active = fields.Boolean('Active',default=True)


class ResPartner(models.Model):
    _inherit = "res.partner"


    doc_count = fields.Integer(compute='_get_doc_count')
    financial_year = fields.Many2one('year.master','Financial Year')
    state = fields.Selection([('to_send', 'To Approve'), ('sent', 'Approved')],string='Statubar',)




class CRM(models.Model):
    _inherit = "crm.lead"

    lead_category = fields.Selection([('hunting','Hunting'),('farming','Farming')],string='Lead Type')
    bottom_line = fields.Float('for Bottom Line')
    date_won = fields.Date('Date won')
    demo_name = fields.Char('Demo')

    crm_bu_id = fields.Many2one('crm.bu',string='BU')
    crm_sub_bu_id = fields.Many2one('crm.sub.bu',string='Sub_Bu')
    financial_year = fields.Many2one('year.master','Financial Year')
    # user_id = fields.Many2one('res.user','crm_lead_user_rel','lead_id','user_id',string="user Id" , copy=False)
    invoice_ids = fields.One2many('crm.invoice','cust_lead_id')

    # quarter = fields.Selection([('q1', 'Quarter-1'), ('q2', 'Quarter-2'), ('q3', 'Quarter-3'), ('q4', 'Quarter-4')],
    #                            string="Quarter", default=_get_quarter)
    state = fields.Selection([('to_send', 'To Send'), ('sent', 'Sent'), ('to_cancel', 'To Cancel'), ('cancelled', 'Cancelled')],string='Statubar',)


    @api.onchange('crm_bu_id')
    def onchabge_sub_id(self):
        for res in self:
            return {'domain':{'crm_sub_bu_id':[('crm_bu_id','=', res.crm_bu_id.id)]}}


    @api.model
    def create(self, vals):
        if vals.get('partner_id'):
            partner_id = self.env['res.partner'].sudo().browse(vals.get('partner_id'))
            if partner_id.parent_id:
                vals['partner_id'] = partner_id.parent_id.id
        res = super(CRM, self).create(vals)
        if res.user_ids:
            for user in res.user_ids:
                res.mail_template(user)
        return res

    def write(self, vals):
        #       Check for the existing user
        existing_users = self.user_ids.ids
        if vals.get('user_ids'):
            users = vals.get('user_ids')[0]
            if users and len(users) == 3:
                user_id = [user for user in users[2] if user not in existing_users]
                User = self.env['res.users'].sudo().browse(user_id)
                for u_id in User:
                    self.mail_template(u_id)
        #       Send mail when satge changed
        # if  vals.get('stage_id'):
        #     for u_id in self.user_ids:
        #         self.mail_template(u_id)
        #     self.mail_template(self.user_id)
        return super(CRM, self).write(vals)


class CrmBu(models.Model):
    _name = 'crm.bu'
    _description = 'Bu for the company'
    crm_bu_id = fields.Many2one('crm.sub.bu')
    name = fields.Char('name',required=True,translate=True)
    active = fields.Boolean('Active',default=True)

class CrmSubBu(models.Model):
    _name = "crm.sub.bu"
    _description = 'su bu for the company'

    name = fields.Char('Name',required=True,translate=True)
    active = fields.Boolean('Active',default=True)
    crm_bu_id = fields.One2many('crm.bu','crm_bu_id')


class CrmInvoice(models.Model):
    _name = 'crm.invoice'
    _description = 'CRM Invoice'

    cust_lead_id = fields.Many2one('crm.lead',string='crm')
    invoice_no = fields.Integer(string='Invoice No')







