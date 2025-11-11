import pytest
from fastapi import status
import json


class TestMainRoutes:
    def test_endpoints(self, client):
        response = client.post(
            "http://localhost:8080/api/v1/wallets/create_wallet/create_wallet",
            json={"amount": "100"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data['amount'] == 100
        id = data['id']
        response = client.get(
            f"http://localhost:8080/api/v1/wallets/{id}"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data['amount'] == 100
        assert data['id'] == id

        response = client.post(
            f"http://localhost:8080/api/v1/wallets/{id}/operation",
            json={"operation_type": "DEPOSIT", "amount": "100"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data['amount'] == 200
        assert data['id'] == id

        response = client.post(
            f"http://localhost:8080/api/v1/wallets/{id}/operation",
            json={"operation_type": "WITHDRAW", "amount": "150"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data['amount'] == 50
        assert data['id'] == id

        response = client.post(
            f"http://localhost:8080/api/v1/wallets/{id}/operation",
            json={"operation_type": "WITHDRAW", "amount": "150"},
        )

        assert response.status_code == status.HTTP_402_PAYMENT_REQUIRED
        data = response.json()

        assert data['amount'] == 50
        assert data['id'] == id

        response = client.post(
            f"http://localhost:8080/api/v1/wallets/{id}/operation",
            json={"operation_type": "DESTROY", "amount": "150"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

        response = client.delete(
            f"http://localhost:8080/api/v1/wallets/{id}"
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.get(
            f"http://localhost:8080/api/v1/wallets/{id}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
