from django.urls import path
from .views import product_list, product_detail

urlpatterns = [
    path("model/<int:model_id>/", product_list, name="product_list"),
    path("detail/<int:product_id>/", product_detail, name="product_detail"),
]