
from django.shortcuts import render
from FilmVaultApp.models import *
import xml.etree.ElementTree as ET
import lxml.etree as LET
<<<<<<< HEAD
from lxml import etree
import feedparser
from FilmVaultApp.myLib.baseXquerys import getFilmsSortedByYear, getFilmXML, getFilmsSortedByAlfa
from django.conf import settings
=======
>>>>>>> 6e568418daec7208a616b56bb2d2ebfd66a564de

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

<<<<<<< HEAD

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

=======
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
>>>>>>> 6e568418daec7208a616b56bb2d2ebfd66a564de
