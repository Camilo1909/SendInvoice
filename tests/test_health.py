"""
Tests para health check endpoints
"""

from django.test import Client
from django.urls import reverse

import pytest


@pytest.mark.django_db
class TestHealthCheck:
    """Tests para endpoints de salud"""

    def test_health_check_returns_200(self):
        """Health check debe retornar 200 OK"""
        client = Client()
        response = client.get("/health/")
        assert response.status_code == 200

    def test_health_check_json_structure(self):
        """Health check debe retornar JSON con estructura correcta"""
        client = Client()
        response = client.get("/health/")
        data = response.json()

        assert "status" in data
        assert "django" in data
        assert data["django"] == "ok"

    def test_liveness_check(self):
        """Liveness check debe retornar 200"""
        client = Client()
        response = client.get("/live/")
        assert response.status_code == 200

    def test_readiness_check(self):
        """Readiness check debe verificar BD"""
        client = Client()
        response = client.get("/ready/")
        assert response.status_code == 200
