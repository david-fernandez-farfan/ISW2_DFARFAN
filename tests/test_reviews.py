from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from relecloud.models import Review, Destination

class ReviewTests(TestCase):

    def test_create_review_simple(self):
        user = User.objects.create_user(username="alice", password="123")
        dest = Destination.objects.create(name="Marte", description="Rojo")

        review = Review.objects.create(
            user=user,
            destination=dest,
            rating=5,
            comment="Increíble!"
        )

        self.assertEqual(review.rating, 5)
        self.assertEqual(review.user, user)
        self.assertEqual(review.destination, dest)

    def test_rating_must_be_between_1_and_5(self):
        user = User.objects.create_user("bob")
        dest = Destination.objects.create(name="Luna", description="Blanca")

        review = Review(
            user=user,
            destination=dest,
            rating=6,
            comment="mal"
        )

        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_average_rating_simple(self):
        u1 = User.objects.create_user("u1")
        u2 = User.objects.create_user("u2")
        dest = Destination.objects.create(name="Saturno", description="Anillos")

        Review.objects.create(user=u1, destination=dest, rating=5)
        Review.objects.create(user=u2, destination=dest, rating=3)

        self.assertEqual(dest.average_rating, 4)
