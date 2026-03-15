from django.urls import path

from . import views


urlpatterns = [
    path("", views.api_root, name="api-root"),
    path("category/", views.category_list, name="category-list"),
    path("category/create/", views.category_create, name="category-create"),
    path("category/<int:id>", views.category_item, name="category-item"),
    path("category/<int:id>/", views.category_item),
    path("product/", views.product_list, name="product-list"),
    path("product/create/", views.product_create, name="product-create"),
    path("product/<int:id>", views.product_item, name="product-item"),
    path("product/<int:id>/", views.product_item),
]
