import xmltodict
from BaseXClient import BaseXClient
from django.db import models
from django.conf import settings
from enum import Enum
from pathlib import Path
import os
from imdb import IMDb


BASE_DIR = Path(__file__).resolve().parent.parent


class UDF():
    filmsByYear = "funcs:filmsOrderByYearPage({}, {} {})"
    filmsByAlfa = "funcs:filmsOrderByAlfaPage({}, {} {})"
    filmXML     = "funcs:getFilm({})"

module_import = "import module namespace funcs = 'funcs' at '" + str(BASE_DIR) + "/querys/funcs.xq'; \n "
query = "xquery {} {}"



def getFilmsSortedByYear(pageIndex, n, syear = None, fyear = None, cat = None):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')


    result = None
    if cat:
        if syear != None and fyear != None:
            q = query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ", {}, {}, {}".format(syear, fyear, cat)))
        else:
            q = query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ", {}".format(cat)))
    else:
        if syear != None and fyear != None:
            q = query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ", {}, {}".format(syear, fyear)))
        else:
            q = query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ''))


    result = session.execute(q)
    dict = xmltodict.parse(result)

    return [movie for movie in dict['root']['elem']]

def getFilmsSortedByAlfa(pageIndex, n, syear = None, fyear = None, cat = None):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')


    q = None
    if cat:
        if syear != None and fyear != None:
            q = query.format(module_import, UDF.filmsByAlfa.format(pageIndex, n, ", {}, {}, {}".format(syear, fyear, cat)))
        else:
            q = query.format(module_import, UDF.filmsByAlfa.format(pageIndex, n, ", {}".format(cat)))
    else:
        if syear != None and fyear != None:
            q = query.format(module_import, UDF.filmsByAlfa.format(pageIndex, n, ", {}, {}".format(syear, fyear)))
        else:
            q = query.format(module_import, UDF.filmsByAlfa.format(pageIndex, n, ''))


    result = session.execute(q)
    dict = xmltodict.parse(result)
    return [movie for movie in dict['root']['elem']]

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

for i in getFilmsSortedByYear(0,50):
    print(i['directors'])
    print("\n")

# print(getFilmXML('0948470'))

#newFilm("9624766")

# newFilm("9624766")


