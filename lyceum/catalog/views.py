import django.shortcuts


items = [1, 2, 3, 4, 5, 6]


def item_list(request):
    template = "catalog/item_list.html"
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, num):
    template = "catalog/item.html"
    context = {"pk": num}
    return django.shortcuts.render(request, template, context)


__all__ = [
    "item_list",
    "item_detail",
]
