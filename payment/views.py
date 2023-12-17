import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from basket.session import Basket
from order.views import payment_confirmation

# This is tested secret API key.
stripe.api_key = 'sk_test_51ONaoGJ7DBfLTFeg1mtFvVrCYWgkHodJxSiaLKuyr7YYP7Ze4HDvIQes8nyEKk8lL5x2oETAfiWLJ5EP6UfQMHSi00s9LubEJl'


@login_required
def basket_view(request):
    basket = Basket(request)
    total_price = str(basket.get_total_price())

    # 创建 Stripe 支付意图
    payment_intent = stripe.PaymentIntent.create(
        amount=int(float(total_price) * 100),
        currency="usd",
        metadata={'user_id': request.user.id},
    )

    return render(request, "payment/home.html", {"client_secret": payment_intent.client_secret})


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/order_placed.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
