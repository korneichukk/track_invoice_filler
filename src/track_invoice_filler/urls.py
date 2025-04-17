from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_track_invoice/", views.create_track_invoice, name="create_new_track_invoice"),
    path(
        "download/<str:company_name>/<str:template_name>",
        views.download_pdf,
        name="download_pdf",
    ),
]
