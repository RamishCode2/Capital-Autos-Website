from django.urls import path
from .views import product_list, product_detail, search_products
from .views import category_list, product_list, product_detail , shop

urlpatterns = [
    path(
        "model/<int:model_id>/",
        category_list,
        name="category_list",
    ),

    path(
        "model/<int:model_id>/category/<int:category_id>/",
        product_list,
        name="product_list",
    ),

    path(
        "detail/<int:product_id>/",
        product_detail,
        name="product_detail",
    ),
    path("search/", search_products, name="search_products"),
    path("shop/", shop, name="shop"),
]