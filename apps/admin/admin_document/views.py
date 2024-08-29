from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import permission_required


@permission_required("document.view_document", raise_exception=True)
def document_list(request):
    return render(request, "admin_document/document/list.html")


@permission_required("document.add_document", raise_exception=True)
def document_add(request):
    return render(request, "admin_document/document/add.html")


# @permission_required('rbac.add_user', raise_exception=True)
# def user_add(request):
#     return render(request, "admin_rbac/user/add.html")


# @permission_required('rbac.change_user', raise_exception=True)
# def user_edit(request, uuid):
#     context = {"uuid": uuid}
#     return render(request, "admin_rbac/user/edit.html", context)
