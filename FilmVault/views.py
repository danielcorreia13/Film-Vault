from django.shortcuts import render
from FilmVault.models import *

# Create your views here.


def home(request):
    return render(request, 'index.html')


def film_results(request, num_page=1):

    dict_list = getFilmsSortedByYear(num_page, 4)
    num_results = int(dict_list[0]['count'])
    num_pages_total = int(num_results/4)+1

    tparams= {
        "dic": dict_list,
        "num_pages_total": num_pages_total,
        "num_page": num_page,
        "pages_inds": range(num_page, num_page+5),
    }

    return render(request, "searchpage.html", tparams)

