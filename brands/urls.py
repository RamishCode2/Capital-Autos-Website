from django.urls import path
from .views import brand_detail, brand_directory

urlpatterns = [
    path("", brand_directory, name="brands"),
    path("<int:brand_id>/", brand_detail, name="brand_detail"),
]
