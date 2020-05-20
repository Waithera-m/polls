from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    """
    view function returns the landing page
    """
    return HttpResponse("Bonjour et bienvue")