from django.shortcuts import render


def handler400(request, *args, **argv):
    return render(request, 'base/handle_errors/400.html')


def handler403(request, *args, **argv):
    return render(request, 'base/handle_errors/403.html')


def handler404(request, *args, **argv):
    return render(request, 'base/handle_errors/404.html')


def handler500(request, *args, **argv):
    return render(request, 'base/handle_errors/500.html')
