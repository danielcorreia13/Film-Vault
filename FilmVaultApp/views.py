
from django.shortcuts import render
from FilmVaultApp.models import *
import xml.etree.ElementTree as ET
import lxml.etree as LET

from lxml import etree
import feedparser
from FilmVaultApp.myLib.baseXquerys import getFilmsSortedByYear, getFilmXML, getFilmsSortedByAlfa
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

import feedparser
from FilmVaultApp.myLib.baseXquerys import getFilmsSortedByYear, getFilmXML, getFilmsSortedByAlfa, newFilm
from django.contrib.auth import authenticate, login, logout
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
    dict_GET = request.GET
    print(dict_GET)
    genres_state = {                        # create state of checkbox genres
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
    }
    dict_list = {}

    if not bool(dict_GET):                  # default query results
        dict_list = getFilmsSortedByYear(num_page, 4)

    else:  # Filters received through GET

        genres = ""
        min_year = None
        max_year = None
        title_search = ""

        for k in dict_GET:
            if k in genres_state:
                genres_state[k] = True
                genres += k +" "            # genres are passed in "g1 g2 g3 (...)" format

        genres = genres[:-1]
        print(genres)

        if 'min_year' in dict_GET and 'max_year' in dict_GET:
            min_year = dict_GET['min_year']
            max_year = dict_GET['max_year']

        if 'title_search' in dict_GET:
            print(dict_GET['title_search'])
            title_search = dict_GET['title_search']

        if 'sort' in dict_GET:
            if dict_GET['sort'] == 'alfa_sort':
                dict_list = getFilmsSortedByAlfa(num_page, 4, min_year, max_year, genres, title_search)
            elif dict_GET['sort'] == 'recent_sort':
                dict_list = getFilmsSortedByYear(num_page, 4, min_year, max_year, genres, title_search)
        else:
            dict_list = getFilmsSortedByYear(num_page, 4, min_year, max_year, genres, title_search)

    num_results = int(dict_list[0]['count'])
    num_pages_total = int(num_results / 4) + 1

    tparams = {
        "dic": dict_list,
        "num_pages_total": num_pages_total,
        "num_page": num_page,
        "pages_inds": range(num_page, num_page + 5),
        "genres": genres_state
    }
    print(genres_state)
    return render(request, "searchpage.html", tparams)


def singlefilm(request, id):

    file = getFilmXML(id)
    root = etree.fromstring(file)
    film = root.find('original-title').text

    xml_f = etree.parse(str(settings.BASE_DIR) + "/querys/uniqueMovie.xsl")
    transform = etree.XSLT(xml_f)
    result = transform(root)

    print("cenas:" + str(result))

    tparams={
        'single_film': result,
        'name': film,
    }

    return render(request,"film.html",tparams)

def logoutView(request):
    logout(request)
    return redirect("login")

def loginView(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("adminpage")
        else:
            return render(request, "login.html",
                          {
                              'error' : True
                          })
    else:
        return render(request,
                      "login.html",
                      {
                          'error' : False
                      })

@login_required
def adminPage(request):
    if 'url' in request.POST:
        url = request.POST['url']
        error = False
        try:
            fields = url.split("/")
            id = fields[4][2:]
            newFilm(id)
        except:
            error = True
        if not error:
            return render(request, "adminpage.html")

        else:
            return render(request, "adminpage.html",
                          {
                              'error' : True
                          })
    else:
        return render(request,
                      "adminpage.html",
                      {
                          'error' : False
                      })
