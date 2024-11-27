from django.shortcuts import render

def vista_administrador(request):
    return render(request, 'admin/base_site.html')