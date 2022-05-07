import json
import uuid
import requests


class PixBot:
    def __init__(self, app_id: str) -> None:
        self.headers = {
            'Authorization': app_id,
            'Content-Type': 'application/json'
        }

    def get_payment_by_id(self, id: uuid.UUID | str) -> requests.Response:
        response = requests.get(
            f'https://api.openpix.com.br/api/openpix/v1/charge/{id}',
            headers=self.headers
        )

        return response

    def create_payment_request(self, amount: int, id: uuid.UUID | str) -> requests.Response:
        payload = {
            'correlationID': id,
            'value': amount,
            'expiresIn': 1200
        }

        response = requests.post(
            'https://api.openpix.com.br/api/openpix/v1/charge?return_existing=true',
            data=json.dumps(payload),
            headers=self.headers
        )

        return response
