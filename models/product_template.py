from odoo import models, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.constrains('categ_id', 'tracking')
    def _check_tracking_for_categories(self):
        for product in self:
            category_name = product.categ_id.name
            if category_name in ['Raw Material', 'Semi-Finished Goods', 'Finished Goods']:
                if product.tracking != 'lot':
                    raise UserError(f"Products in category '{category_name}' MUST be tracked by lot.")

# DESCRIPTION AND COMMENTS
# We inherit product.template to introduce an @api.constrains constraint.
# Whenever the category (categ_id) or tracking fields change, this method evaluates the product.
# If the product's category matches one of our target 3 categories, the tracking 
# is strictly required to be 'lot'. If it's not, a UserError is raised to prevent saving.
