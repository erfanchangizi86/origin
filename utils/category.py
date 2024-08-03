from products.models import category


def get_subcategories(value):
    subcategories = value.children.all()
    subcategories_data = []

    for subcategory in subcategories:
        subcategories_data.append({
            'id': subcategory.id,
            'name': subcategory.title,
            'url_name': subcategory.url_name,
            'subcategories': get_subcategories(subcategory)
        })

    return subcategories_data


# Create your views here.

def get_all_categories():
    categories = category.objects.filter(is_active=True, is_deleted=False,title_category=None)  # دسته‌بندی‌های اصلی
    data = []
    for cate_gory in categories:
        data.append({
            'id': cate_gory.id,
            'name': cate_gory.title,
            'url_name': cate_gory.url_name,
            'subcategories': get_subcategories(cate_gory)
        })

    return data



