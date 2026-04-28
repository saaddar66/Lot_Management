from odoo import models, api

class StockLot(models.Model):
    _inherit = 'stock.lot'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == '/':
                if 'product_id' in vals:
                    product = self.env['product.product'].browse(vals['product_id'])
                    if product.categ_id.name == 'Raw Material':
                        vals['name'] = self.env['ir.sequence'].next_by_code('lot.sequence.raw') or '/'
                    elif product.categ_id.name in ['Semi-Finished Goods', 'Finished Goods']:
                        vals['name'] = self.env['ir.sequence'].next_by_code('lot.sequence.finished') or '/'
        return super(StockLot, self).create(vals_list)

# DESCRIPTION AND COMMENTS
# By inheriting stock.lot and overriding the create method, we hook into 
# the lot creation process across the system. If no specific name is provided 
# (or the placeholder '/' is given), we inspect the product's category.
# Based on the category, we pull the next number from our respective custom sequence.
