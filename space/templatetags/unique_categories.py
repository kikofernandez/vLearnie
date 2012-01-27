from django import template
register = template.Library()

def remove_repeated_categories(object_list):
    set_categories = set()
    for entry in object_list:
        set_categories.update(entry.categories.all())
    return set_categories
register.filter('remove_repeated_categories', remove_repeated_categories)