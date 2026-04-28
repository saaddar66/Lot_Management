from odoo import models, api

class StockLot(models.Model):
    _inherit = 'stock.lot'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Check if name is default or missing
            if not vals.get('name') or vals.get('name') == '/':
                if 'product_id' in vals:
                    product = self.env['product.product'].browse(vals['product_id'])
                    category = product.categ_id.name
                    
                    # Triple logic split for categories
                    if category == 'Raw Material':
                        vals['name'] = self.env['ir.sequence'].next_by_code('lot.sequence.raw') or '/'
                    elif category == 'Semi-Finished Goods':
                        vals['name'] = self.env['ir.sequence'].next_by_code('lot.sequence.semi') or '/'
                    elif category == 'Finished Goods':
                        vals['name'] = self.env['ir.sequence'].next_by_code('lot.sequence.finished') or '/'
                        
        return super(StockLot, self).create(vals_list)

# DESCRIPTION AND COMMENTS
# The create method of stock.lot is overridden to handle manual or background creation.
# It checks the category of the product and assigns a sequence-based name if one isn't provided.
# We now support three distinct sequences: Raw (1...), Semi (2...), and Finished (3...).
