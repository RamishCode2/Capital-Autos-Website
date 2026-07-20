from django.urls import path
from .views import brand_detail

urlpatterns = [
    path("<int:brand_id>/", brand_detail, name="brand_detail"),
]