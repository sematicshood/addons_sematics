from flectra import models, fields, api
import requests
from ast import literal_eval
import json
import string
import random

class Invoice(models.Model):
    _inherit        =   'account.invoice'

    redirect_url    =   fields.Text()
    token           =   fields.Text()

    def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
    @api.model
    def get_link_midtrans(self):
        if self[0].redirect_url is False:
            data = {
                        "transaction_details": {
                            "order_id": self[0].number,
                            "gross_amount": round(self[0].amount_total)
                        }, "credit_card":{
                            "secure" : True
                        }
                    }
            link = 'http://localhost:7073/sematics_api/midtrans/payment_link'

            request_link = requests.get(link, json = data)
            response     = json.loads(request_link._content.decode('utf-8'))['result']

            self[0].write({
                'token': response['token'],
                'redirect_url': response['redirect_url']
            })

            return response['redirect_url']
        else:
            return self[0].redirect_url