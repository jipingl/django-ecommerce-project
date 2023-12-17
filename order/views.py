from django.http import JsonResponse
from django.shortcuts import render

from basket.session import Basket
from order.models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        user_id = request.user.id
        total_price = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            # 创建订单
            order = Order.objects.create(user_id=user_id, full_name=full_name, address1=address, post_code=postcode,
                                         address2='address2', total_paid=total_price, order_key=order_key)
            order_id = order.pk
            # 创建订单项
            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'],
                                         quantity=item['qty'])
        return JsonResponse({'success': 'Return something'})


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
