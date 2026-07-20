from django.urls import path
from .views import product_list

urlpatterns = [
    path("model/<int:model_id>/", product_list, name="product_list"),
]