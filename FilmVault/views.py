from django.shortcuts import render
from FilmVault.models import *
import xml.etree.ElementTree as ET
import lxml.etree as LET #to use on xslt
import feedparser

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

