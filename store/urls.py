from django.urls import path

from store import views

app_name = "store"

urlpatterns = [
    path("", views.all_products, name="all_products"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail")
]
