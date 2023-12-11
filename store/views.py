from django.shortcuts import render, get_object_or_404

from store.models import Product, Category


def all_products(request):
    products = Product.products.filter()
    return render(request, "store/home.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, "store/products/detail.html", {"product": product})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, "store/products/category.html", {"category": category, "products": products})
