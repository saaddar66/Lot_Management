from odoo import models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        # Ensure lots are populated for incoming receipts
        for picking in self:
            if picking.picking_type_id.code == 'incoming':
                for move_line in picking.move_line_ids:
                    product = move_line.product_id
                    category = product.categ_id.name
                    
                    if category in ['Raw Material', 'Semi-Finished Goods', 'Finished Goods']:
                        # Only generate if both lot_id and lot_name are missing
                        if not move_line.lot_id and not move_line.lot_name:
                            
                            # Triple logic split for sequences
                            if category == 'Raw Material':
                                lot_name = self.env['ir.sequence'].next_by_code('lot.sequence.raw')
                            elif category == 'Semi-Finished Goods':
                                lot_name = self.env['ir.sequence'].next_by_code('lot.sequence.semi')
                            elif category == 'Finished Goods':
                                lot_name = self.env['ir.sequence'].next_by_code('lot.sequence.finished')
                            
                            move_line.lot_name = lot_name
        
        return super(StockPicking, self).button_validate()

# DESCRIPTION AND COMMENTS
# The button_validate method in stock.picking is updated to support the new triple sequence logic.
# When validating a Receipt, it automatically generates lot numbers for Raw Materials,
# Semi-Finished, or Finished goods if they are missing. This ensures traceability 
# from the moment items enter the warehouse.
