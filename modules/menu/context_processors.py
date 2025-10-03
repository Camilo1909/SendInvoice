# menu/context_processors.py
from .models import MenuItem


def menu_items(request):
    return {"menu_items": MenuItem.get_items_for_user(request)}
