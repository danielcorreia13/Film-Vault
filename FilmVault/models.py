import xmltodict
from BaseXClient import BaseXClient
from django.db import models
from django.conf import settings
from enum import Enum
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent


class UDF():
    filmsByYear = "funcs:filmsOrderByYearPage({}, {} {})"


module_import = "import module namespace funcs = 'funcs' at '" + str(BASE_DIR) + "/querys/funcs.xq'; \n "
query = "xquery {} {}"



def getFilmsSortedByYear(pageIndex, n, syear = None, fyear = None, cat = None):
    session = BaseXClient.Session('192.168.1.196', 1984, 'admin', 'admin')


    result = None
    if cat:
        if syear != None and fyear != None:
            result = session.execute(query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ", {}, {}, {}".format(syear, fyear, cat))))
        else:
            result = session.execute(query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ", {}".format(cat))))
    else:
        if syear != None and fyear != None:
            result = session.execute(query.format(module_import, UDF.filmsByYear.format(pageIndex, n, ", {}, {}".format(syear, fyear))))
        else:
            result = session.execute(query.format(module_import, UDF.filmsByYear.format(pageIndex, n, '')))

    dict = xmltodict.parse(result)

    return [movie for movie in dict['root']['elem']]

<<<<<<< HEAD
getFilmsSortedByYear(0,10)
=======
>>>>>>> querys
