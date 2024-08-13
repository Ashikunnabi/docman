from django.contrib.auth.decorators import permission_required
from django.shortcuts import render



@permission_required("inventory.view_menu", raise_exception=True)
def menu_list(request):
    return render(request, "admin_menu/menu/list.html")


@permission_required("inventory.view_menu", raise_exception=True)
def menu_add(request):
    return render(request, "admin_menu/menu/add.html")


@permission_required("inventory.view_menu", raise_exception=True)
def menu_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_menu/menu/edit.html", context)

@permission_required("inventory.view_menutype", raise_exception=True)
def menu_type_list(request):
    return render(request, "admin_menu/menu_type/list.html")


@permission_required("inventory.view_menutype", raise_exception=True)
def menu_type_add(request):
    return render(request, "admin_menu/menu_type/add.html")


@permission_required("inventory.view_menutype", raise_exception=True)
def menu_type_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_menu/menu_type/edit.html", context)