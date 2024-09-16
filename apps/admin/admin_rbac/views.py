from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.decorators import permission_required

"""
===============================================================================
                                    USER
===============================================================================
"""

@permission_required('rbac.view_user', raise_exception=True)
def user_list(request):
    return render(request, "admin_rbac/user/list.html")


@permission_required('rbac.add_user', raise_exception=True)
def user_add(request):
    return render(request, "admin_rbac/user/add.html")


@permission_required('rbac.change_user', raise_exception=True)
def user_edit(request, uuid):
    context = {"uuid": uuid}
    return render(request, "admin_rbac/user/edit.html", context)


"""
===============================================================================
                                    GROUP
===============================================================================
"""


@permission_required('auth.view_group', raise_exception=True)
def group_list(request):
    return render(request, "admin_rbac/group/list.html")


@permission_required('auth.add_group', raise_exception=True)
def group_add(request):
    return render(request, "admin_rbac/group/add.html")


@permission_required('auth.change_group', raise_exception=True)
def group_edit(request, id):
    context = {"id": id}
    return render(request, "admin_rbac/group/edit.html", context)


"""
===============================================================================
                            USER ACTIVITY LOG
===============================================================================
"""


def user_activity_log_list(request):
    return HttpResponse(
        "<h1>UNAUTHORIZED</h1> You have no access. Ask admin to get access."
    )
    return render(request, "admin_rbac/activity_log/list.html")
