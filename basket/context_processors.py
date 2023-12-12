from basket.session import Basket


def basket(request):
    return {'basket': Basket(request)}
