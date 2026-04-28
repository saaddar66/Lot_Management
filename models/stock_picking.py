from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        # Before validation logic executes, ensure lots are populated
        for picking in self:
            # Check if this is an incoming receipt
            if picking.picking_type_id.code == 'incoming':
                for move_line in picking.move_line_ids:
                    product = move_line.product_id
                    if product.categ_id.name in ['Raw Material', 'Semi-Finished Goods', 'Finished Goods']:
                        # If a lot number hasn't been manually assigned yet
                        if not move_line.lot_id and not move_line.lot_name:
                            # Automatically fetch the next lot sequence
                            if product.categ_id.name == 'Raw Material':
                                lot_name = self.env['ir.sequence'].next_by_code('lot.sequence.raw')
                            else:
                                lot_name = self.env['ir.sequence'].next_by_code('lot.sequence.finished')
                            
                            move_line.lot_name = lot_name
        
        # Proceed with normal validation
        return super(StockPicking, self).button_validate()

# DESCRIPTION AND COMMENTS
# Here we inherit stock.picking and override button_validate.
# During a receipt validation, we iterate over the stock move lines.
# If a line concerns one of our targeted categories and is missing a lot number,
# we generate and assign the sequence name dynamically to the lot_name field.
# Odoo handles creating the actual stock.lot records based on this lot_name during validation.
