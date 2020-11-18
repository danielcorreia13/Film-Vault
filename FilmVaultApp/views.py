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