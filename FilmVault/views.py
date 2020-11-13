from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'index.html')

def searchpage(request):
    tparams = {}
    return render(request, 'searchpage.html')

def filmsResults(request,num_films, ):

    tparams= {
        'imgs':,
        'titles':,
        'years':,
        'genres':,
        'actors':,
        'directors':,
        'ratings':,
        'num_films':range(num_films),

    }