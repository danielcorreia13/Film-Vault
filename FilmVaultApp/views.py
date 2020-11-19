from django.shortcuts import render
from FilmVaultApp.models import *
import xml.etree.ElementTree as ET
import lxml.etree as LET
import feedparser
from FilmVaultApp.myLib.baseXquerys import getFilmsSortedByYear, getFilmXML, getFilmsSortedByAlfa

# Create your views here.


def home(request):
    feeds = feedparser.parse("https://screenrant.com/feed/")
    filmNews = []
    for feed in feeds["entries"]:
        if len(filmNews) < 6:
            filmNews.append({
                "title": feed["title"],
                "link": feed["link"],
                "description": feed["summary"].replace("&#039;", "'"),
                "imglink": feed["content"][0]["value"].split('"')[1::2][0],
                "pubdate": feed["published"]
            })

    tparams = {
        "news": filmNews,
        "numofnews": 3
    }

    return render(request, "homepage.html", tparams)


def film_results(request, num_page=1):

    genres_state = {}

    if not bool(request.GET):
        genres_state.update({
            "Action": False,
            "Comedy": False,
            "Crime": False,
            "Thriller": False,
            "Horror": False,
            "Musical": False,
            "Romance": False,
            "Biography": False,
            "Drama": False,
            "History": False,
            "Animation": False,
            "Adventure": False,
            "Family": False,
            "Fantasy": False,
            "Sci-Fi": False,
            "Western": False,
            "Film-Noir": False,
            "Mystery": False,
            "Music": False,
            "Sport": False,
            "War": False,
            "Documentary": False,
            "Short": False,
            "News": False
        })
        if 'alfa' in request.GET:
            dict_list = getFilmsSortedByAlfa(num_page, 4)
        else:
            dict_list = getFilmsSortedByYear(num_page, 4)

    else:
        for k, v in request.GET:
            genres_state[k] = True




    dict_list = getFilmsSortedByYear(num_page, 4)
    num_results = int(dict_list[0]['count'])
    num_pages_total = int(num_results/4)+1

    tparams= {
        "dic": dict_list,
        "num_pages_total": num_pages_total,
        "num_page": num_page,
        "pages_inds": range(num_page, num_page+5),
        "genres": ["Action", "Comedy", "Crime", "Thriller", "Horror", "Musical", "Romance", "Biography", "Drama", "History", "Animation", "Adventure", "Family", "Fantasy", "Sci-Fi", "Western", "Film-Noir", "Mystery", "Music", "Sport", "War", "Documentary", "Short", "News"],
    }

    return render(request, "searchpage.html", tparams)

