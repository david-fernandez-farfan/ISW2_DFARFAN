from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

class InfoRequestEmailTests(TestCase):

    @patch("relecloud.views.send_mail")
    def test_view_calls_send_mail(self, mock_send_mail):

        data = {
            "name": "Ana",
            "email": "ana@example.com",
            "message": "Hola"
        }

        self.client.post(reverse("info_request"), data)

        # Verifica que al menos se llamó una vez
        self.assertGreaterEqual(mock_send_mail.call_count, 1)
