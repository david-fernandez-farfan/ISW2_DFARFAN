from django.urls import path
from . import views
from .views import ReviewCreateView

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),

    # ---- REVIEWS SIEMPRE VAN ARRIBA ----
    path(
        "destination/<int:destination_id>/review/",
        ReviewCreateView.as_view(),
        name="add_review_destination",
    ),
    path(
        "cruise/<int:cruise_id>/review/",
        ReviewCreateView.as_view(),
        name="add_review_cruise",
    ),

    # Destinations & Cruises (después)
    path("destinations/", views.destinations, name="destinations"),
    path("destination/<int:pk>/", views.DestinationDetailView.as_view(), name="destination_detail"),
    path("cruise/<int:pk>/", views.CruiseDetailView.as_view(), name="cruise_detail"),

    # Info Request
    path("info-request/", views.info_request_view, name="info_request"),
    path("info-request/success/", views.success_view, name="info_request_success"),
]
