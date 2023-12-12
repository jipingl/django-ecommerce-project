from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from basket.session import Basket
from store.models import Product


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        response = JsonResponse({'basket_qty': basket.__len__()})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product_id=product_id)
        response = JsonResponse({'basket_qty': basket.__len__(), 'total_price': basket.get_total_price()})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        qty = int(request.POST.get('qty'))
        basket.update(product_id=product_id, qty=qty)
        response = JsonResponse({'basket_qty': basket.__len__(), 'total_price': basket.get_total_price()})
        return response
