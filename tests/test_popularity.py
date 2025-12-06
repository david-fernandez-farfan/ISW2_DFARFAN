from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from relecloud.models import Destination, Review

class DestinationPopularityTests(TestCase):
    def setUp(self):
        # Usuario para las reviews
        self.user = User.objects.create_user(username="user1", password="test1234")

        # Dos destinos
        self.dest1 = Destination.objects.create(
            name="Destino A",
            description="Desc A",
        )
        self.dest2 = Destination.objects.create(
            name="Destino B",
            description="Desc B",
        )

    def test_destinations_are_ordered_by_popularity(self):
        """
        Destino B tendrá MÁS reviews que Destino A, por tanto debe aparecer primero
        en la vista 'destinations'.
        """

        # Destino B: 2 reviews
        Review.objects.create(user=self.user, destination=self.dest2, rating=5)
        Review.objects.create(user=self.user, destination=self.dest2, rating=4)

        # Destino A: 1 review
        Review.objects.create(user=self.user, destination=self.dest1, rating=5)

        response = self.client.get(reverse("destinations"))
        self.assertEqual(response.status_code, 200)

        destinations = list(response.context["destinations"])

        # Primero debe ir B (más popular), luego A
        self.assertEqual(destinations[0].name, "Destino B")
        self.assertEqual(destinations[1].name, "Destino A")