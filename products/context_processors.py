from .models import Category

def product_categories(request):
    """ this context processor adds the list of available product caregories to tge context. It is required by the search feature.
    """
    try:
        res = Category.objects.all()
        return {"categories":res}
    except:
        return {}
