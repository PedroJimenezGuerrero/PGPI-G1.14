from django.shortcuts import render

def vista_administrador(request):
    return render(request, 'admin/base-site.html')