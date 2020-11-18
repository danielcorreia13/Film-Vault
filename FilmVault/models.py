import xmltodict
from BaseXClient import BaseXClient
from django.db import models
from django.conf import settings
from enum import Enum
from pathlib import Path
import os
from imdb import IMDb
from lxml import etree

BASE_DIR = Path(__file__).resolve().parent.parent


class UDF():
    filmsByYear = "funcs:filmsOrderByYearPage({}, {} {})"
    filmsByAlfa = "funcs:filmsOrderByAlfaPage({}, {} {})"
    filmXML     = "funcs:getFilm({})"

module_import = "import module namespace funcs = 'funcs' at '" + str(BASE_DIR) + "/querys/funcs.xq'; \n "
query = "xquery {} {}"

def executeQuery(funcSrt, pageIndex, n, syear = None, fyear = None, cat = None):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    result = None
    pageIndex -= 1
    if cat:
        if syear != None and fyear != None:
            q = query.format(module_import, funcSrt.format(pageIndex, n, ", {}, {}, {}".format(syear, fyear, cat)))
        else:
            q = query.format(module_import, funcSrt.format(pageIndex, n, ", {}".format(cat)))
    else:
        if syear != None and fyear != None:
            q = query.format(module_import, funcSrt.format(pageIndex, n, ", {}, {}".format(syear, fyear)))
        else:
            q = query.format(module_import, funcSrt.format(pageIndex, n, ''))

    result = session.execute(q)
    dict = xmltodict.parse(result)
    if not dict['root']:
        return None
    return [movie for movie in dict['root']['elem']]

def getFilmsSortedByYear(pageIndex, n, syear = None, fyear = None, cat = None):
    return executeQuery(UDF.filmsByYear, pageIndex, n, syear, fyear, cat)

def getFilmsSortedByAlfa(pageIndex, n, syear = None, fyear = None, cat = None):
    return executeQuery(UDF.filmsByAlfa, pageIndex, n, syear, fyear, cat)

def getFilmXML(id):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    result = session.execute(query.format(module_import, UDF.filmXML.format(str(id))))


    return result

def newFilm(id):
    print(id)
    ia = IMDb('https')
    movie = ia.get_movie(str(id))
    xml = movie.asXML(_with_add_keys=False)
    print(xml)
    tree = etree.fromstring(xml)
    print(tree)

for i in getFilmsSortedByYear(100,2,1997, 2002):
    print(i)
    print("\n")

# print(getFilmXML('0948470'))

#newFilm("9624766")

# newFilm("9624766")


