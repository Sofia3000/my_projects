from .models import Category
def get_categories():
    categories = Category.objects.all().values('id', 'name')
    categories_list = [(c['id'], c['name']) for c in categories]
    categories_list.insert(0, (None, "No category"))
    return tuple(categories_list)