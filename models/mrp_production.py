from odoo import models, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        # We removed the lot generation logic from here to satisfy the new requirement
        # of triggering it only during production/recording.
        return super(MrpProduction, self).action_confirm()

    def button_mark_done(self):
        """
        Trigger lot generation only when the production is being finalized
        (clicking Produce/Mark as Done).
        """
        for production in self:
            if production.product_id.tracking == 'lot' and not production.lot_producing_id:
                category = production.product_id.categ_id.name
                seq_code = False
                
                # Determine sequence based on category
                if category == 'Finished Goods':
                    seq_code = 'lot.sequence.finished'
                elif category == 'Semi-Finished Goods':
                    seq_code = 'lot.sequence.semi'
                
                if seq_code:
                    lot_name = self.env['ir.sequence'].next_by_code(seq_code)
                    if lot_name:
                        # Create and assign the lot
                        lot = self.env['stock.lot'].create({
                            'name': lot_name,
                            'product_id': production.product_id.id,
                            'company_id': production.company_id.id,
                        })
                        production.lot_producing_id = lot.id
                        
        return super(MrpProduction, self).button_mark_done()

# DESCRIPTION AND COMMENTS
# In this version, we moved the automation logic from 'action_confirm' to 'button_mark_done'.
# This ensures that the lot number is only generated when the production is actually completed.
# It specifically targets Finished and Semi-Finished goods produced via MOs.
# Raw Materials are handled by the Receipt (stock.picking) logic instead.
