from django.urls import path

from . import views

urlpatterns = [
    path("classify/", views.classify_patient_state, name="classify"),
    path("coverage/", views.coverage, name="coverage"),
    path("generate/", views.generate, name="generate"),
]
