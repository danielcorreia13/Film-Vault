from django.shortcuts import render
from FilmVault.models import *

# Create your views here.

def home(request):
    return render(request, 'index.html')

def searchpage(request):
    tparams = {}
    return render(request, 'searchpage.html')

def filmsResults(request):

    dic = getFilmsSortedByYear(0, 4)
    print(dic)
    tparams= {
        "dic": dic,
    }

    return render(request,"searchpage.html",tparams)

#def filmDic()

