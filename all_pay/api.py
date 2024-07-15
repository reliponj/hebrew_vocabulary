import hashlib

import requests
from django.conf import settings

from payment.models import Payment


class AllPayAPI:
    _login = settings.ALLPAY_LOGIN
    _api_key = settings.ALLPAY_API_KEY

    def get_sign(self, data):
        sorted_params = sorted(data.items())
        chunks = []

        for k, v in sorted_params:
            v = v.strip()
            if v != '' and k != 'sign':
                chunks.append(v)

        signature_string = ':'.join(chunks) + ':' + self._api_key
        signature = hashlib.sha256(signature_string.encode()).hexdigest()
        return signature

    def create_payment(self, payment: Payment, callback_url):
        url = "https://allpay.to/app/?show=getpayment&mode=api5"
        data = {
            "name": f"Оплата подписки #{payment.id} - {payment.user.email}",
            "login": self._login,
            "order_id": f'{payment.id}',
            "amount": f'{payment.sum}',
            "notifications_url": callback_url,

            "client_name": payment.user.email,
            "client_email": payment.user.email,
        }
        data['sign'] = self.get_sign(data)

        response = requests.post(url, data=data).json()
        return response['payment_url']
