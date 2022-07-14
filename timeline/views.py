from django.http import HttpResponse
from django.shortcuts import render

def principal (request):
    return render(request, 'timeline/principal.html')