from .models import Catagory

def AllCatagory(request):
    context = {
        'all_catagory' : Catagory.objects.all()
    }
    return context
