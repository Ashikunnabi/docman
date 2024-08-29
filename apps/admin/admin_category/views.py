from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import permission_required



@permission_required("category.edit_category", raise_exception=True)
def category_edit(request, uuid):
    return render(request, "admin_category/category/edit.html", context={"uuid": uuid})


# @permission_required('rbac.add_user', raise_exception=True)
# def user_add(request):
#     return render(request, "admin_rbac/user/add.html")


# @permission_required('rbac.change_user', raise_exception=True)
# def user_edit(request, uuid):
#     context = {"uuid": uuid}
#     return render(request, "admin_rbac/user/edit.html", context)
