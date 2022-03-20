# -*- coding: utf-8 -*-
from odoo import http

# class BookingOrderHenrotanjung19032022(http.Controller):
#     @http.route('/booking_order_henrotanjung_19032022/booking_order_henrotanjung_19032022/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order_henrotanjung_19032022/booking_order_henrotanjung_19032022/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order_henrotanjung_19032022.listing', {
#             'root': '/booking_order_henrotanjung_19032022/booking_order_henrotanjung_19032022',
#             'objects': http.request.env['booking_order_henrotanjung_19032022.booking_order_henrotanjung_19032022'].search([]),
#         })

#     @http.route('/booking_order_henrotanjung_19032022/booking_order_henrotanjung_19032022/objects/<model("booking_order_henrotanjung_19032022.booking_order_henrotanjung_19032022"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order_henrotanjung_19032022.object', {
#             'object': obj
#         })