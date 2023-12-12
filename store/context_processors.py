from store.models import Category


def categories(request):
    return {"categories": Category.objects.all()}


def product_select_list(request):
    return {"product_select_list": range(1, 6)}
