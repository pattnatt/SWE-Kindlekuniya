from .models import Catagory
from .views import get_product_count_in_cart

def IndexPage(request):
    context = {
        'all_catagory' : Catagory.objects.all(),
        'product_count' : get_product_count_in_cart(request),
    }
    return context
