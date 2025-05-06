from django.shortcuts import render

def mi_error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def mi_error_500(request):
    return render(request, 'errors/500.html', status=500)

def mi_error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def mi_error_400(request, exception):
    return render(request, 'errors/400.html', status=400)