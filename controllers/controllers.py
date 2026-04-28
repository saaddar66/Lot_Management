# -*- coding: utf-8 -*-
# from odoo import http


# class LotManagement(http.Controller):
#     @http.route('/lot_management/lot_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lot_management/lot_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lot_management.listing', {
#             'root': '/lot_management/lot_management',
#             'objects': http.request.env['lot_management.lot_management'].search([]),
#         })

#     @http.route('/lot_management/lot_management/objects/<model("lot_management.lot_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lot_management.object', {
#             'object': obj
#         })

