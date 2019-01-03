# -*- coding: utf-8 -*-

from flectra import models, fields, api

class library_api_sematics(models.Model):
    _name = 'library_api_sematics'

    access_token_bitly = fields.Text(string='API Access Token Bitly.com')