# -*- coding: utf-8 -*-

from flectra import models, fields, api

class library_api_sematics(models.Model):
    _name = 'library_api_sematics'

    host                  = fields.Text()
    access_token_bitly    = fields.Text()
    midtrans_merchant_id  = fields.Text()
    midtrans_client_key   = fields.Text()
    midtrans_server_key   = fields.Text()
    production_midtrans   = fields.Boolean(default=True)
    