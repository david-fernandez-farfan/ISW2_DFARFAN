from django.test import TestCase, override_settings
from django.urls import reverse
from django.core import mail
from app.models import InfoRequest  # ajusta la app según tu proyecto

@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class InfoRequestEmailTests(TestCase):

    def test_valid_request_sends_email(self):
        data = {
            "name": "Ana",
            "email": "ana@example.com",
            "message": "Quiero información"
        }

        response = self.client.post(reverse("info_request"), data)

        # Redirección exitosa
        self.assertEqual(response.status_code, 302)

        # Se guardó la solicitud
        self.assertEqual(InfoRequest.objects.count(), 1)

        # Se envió exactamente 1 email
        self.assertEqual(len(mail.outbox), 1)

        # El email contiene información de la solicitud
        self.assertIn("Ana", mail.outbox[0].body)
