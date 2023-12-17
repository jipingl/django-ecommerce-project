from django.urls import path

from payment import views

app_name = "payment"

urlpatterns = [
    path("", views.basket_view, name="basket"),
    path("order_placed/", views.order_placed, name='order_placed'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]
