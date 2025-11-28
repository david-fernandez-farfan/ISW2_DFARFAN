import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from relecloud.models import Review, Destination, Cruise

@pytest.mark.django_db
def test_create_review():
    user = User.objects.create_user(username="alice", password="123")
    dest = Destination.objects.create(
        name="Marte", description="Rojo"
    )

    review = Review.objects.create(
        user=user,
        destination=dest,
        rating=5,
        comment="Increíble!"
    )

    assert review.rating == 5
    assert review.user == user


@pytest.mark.django_db
def test_rating_range():
    user = User.objects.create_user("bob")
    dest = Destination.objects.create(name="Luna", description="Blanca")

    with pytest.raises(ValidationError):
        Review(
            user=user,
            destination=dest,
            rating=6,
            comment="mal"
        ).full_clean()


@pytest.mark.django_db
def test_user_must_have_purchase():
    user = User.objects.create_user("carl")
    dest = Destination.objects.create(name="Europa", description="Hielo")

    # Usuario NO ha comprado → debe fallar
    with pytest.raises(PermissionDenied):
        Review.objects.create_review(
            user=user,
            destination=dest,
            rating=4,
            comment="Cool"
        )


@pytest.mark.django_db
def test_average_rating():
    u1 = User.objects.create_user("u1")
    u2 = User.objects.create_user("u2")
    dest = Destination.objects.create(name="Saturno", description="Anillos")

    Review.objects.create(user=u1, destination=dest, rating=5)
    Review.objects.create(user=u2, destination=dest, rating=3)

    assert dest.average_rating == 4
