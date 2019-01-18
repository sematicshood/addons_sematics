from flectra import http
from flectra.http import request
import requests
import json
import urllib.parse
from urllib.parse import urlencode
import socket
import datetime
import sys
from midtransclient import Snap, CoreApi
import string
import random
from openerp.osv.orm import except_orm

class Midtrans(http.Controller):
    core = ''
    snap = ''

    def __init__(self, *args, **kwargs):
        self.core = CoreApi(
            is_production=self.is_production(),
            server_key=self.get_server(),
            client_key=self.get_client(),
        )

        self.snap = Snap(
            is_production=self.is_production(),
            server_key=self.get_server(),
            client_key=self.get_client(),
        )
        

    def get_client(self):
        options =   request.env['library_api_sematics'].search_read([])

        return options[0]['midtrans_client_key']

    def get_server(self):
        options =   request.env['library_api_sematics'].search_read([])

        return options[0]['midtrans_server_key']

    def is_production(self):
        options =   request.env['library_api_sematics'].search_read([])

        return options[0]['production_midtrans']

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    """
        Example Response Create Payment Link (VT-LINK)

        {
            'token': '83fdc390-48bb-495a-b201-7e17a82265af', 
            'redirect_url': 'https://app.sandbox.midtrans.com/snap/v2/vtweb/83fdc390-48bb-495a-b201-7e17a82265af'
        }
    """

    @http.route('/sematics_api/midtrans/payment_link', methods=["GET"], type='json', auth="none", csrf=False, cors="*")
    def payment_link(self, **params):
        snap = Snap(
            is_production=False,
            server_key=self.get_server(),
            client_key=self.get_client(),
        )
        """
            Please read manual documentation from midtrans
            https://snap-docs.midtrans.com/#request-body-json-parameter

            Example body json
            {
                "transaction_details": {
                    "order_id": "self.id_generator()",
                    "gross_amount": 21321
                }, "credit_card":{
                    "secure" : "True"
                }
            }
        """
        try:
            transaction_token = self.snap.create_transaction(json.loads(request.httprequest.data))
        except Exception as identifier:
            raise osv.except_osv(_("Error!"), _(identifier))

            return True

        return transaction_token


    """
        Example Response Notification

        {
            "transaction_time": "2019-01-18 09:43:33",
            "transaction_status": "settlement",
            "transaction_id": "d030a126-0571-491d-9d02-579d9fe548f2",
            "status_message": "midtrans payment notification",
            "status_code": "200",
            "signature_key": "1be6f10aa7e7f37eb68ab9aed62f87ffe8f6921f5d39295def4f752f2ecfb1c01c6ba3d3c23b0e257c8e8ae9714b795ad9b909309eee2f6cf7f3877ae1b2bf2c",
            "settlement_time": "2019-01-18 09:43:49",
            "payment_type": "bca_klikpay",
            "order_id": "I8HKV4",
            "gross_amount": "200000.00",
            "fraud_status": "accept",
            "approval_code": "112233"
        }
    """
    @http.route('/sematics_api/midtrans/notification', methods=["POST", "GET"], type='json', auth="none", csrf=False, cors="*")
    def confirm_payment_json(self, **params):
        status_response = json.loads(request.httprequest.data)

        order_id = status_response['order_id']
        transaction_status = status_response['transaction_status']
        gross_amount = status_response['gross_amount']

        # Sample transaction_status handling logic

        if transaction_status == 'settlement':
            settlement_time = status_response['settlement_time']
            
            invoice     = request.env['account.invoice'].sudo().search([('number','=',order_id)])[0]
            pay_journal = request.env['account.journal'].sudo().search([('name','=','Bank')])[0]
            invoice.pay_and_reconcile(pay_journal.id,gross_amount,settlement_time)

        return True