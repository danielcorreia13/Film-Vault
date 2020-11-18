import xmltodict
from BaseXClient import BaseXClient
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class UDF():
    filmsByYear = "funcs:filmsOrderByYearPage({}, {}, {} {})"
    filmsByAlfa = "funcs:filmsOrderByAlfaPage({}, {}, {} {})"
    filmXML     = "funcs:getFilm({})"
    insertFilm  = "funcs:newFilm({}, {})"

module_import = "import module namespace funcs = 'funcs' at '" + str(BASE_DIR) + "/querys/funcs.xq'; \n "
query = "xquery {} {}"

def executeQuery(funcSrt, pageIndex, n, syear = None, fyear = None, cat = None, search = ''):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    result = None
    pageIndex -= 1
    search = "'{}'".format(search)
    cat = "'{}'".format(cat)
    if cat:
        if syear != None and fyear != None:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ", {}, {}, {}".format(syear, fyear, cat)))
        else:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ", {}".format(cat)))
    else:
        if syear != None and fyear != None:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ", {}, {}".format(syear, fyear)))
        else:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ''))
    print(q)
    result = session.execute(q)
    dict = xmltodict.parse(result)
    if not dict['root']:
        return None
    return [movie for movie in dict['root']['elem']]

def getFilmsSortedByYear(pageIndex, n, syear = None, fyear = None, cat = None, search = ""):
    return executeQuery(UDF.filmsByYear, pageIndex, n, syear, fyear, cat, search)

def getFilmsSortedByAlfa(pageIndex, n, syear = None, fyear = None, cat = None, search = ""):
    return executeQuery(UDF.filmsByAlfa, pageIndex, n, syear, fyear, cat, search)

def getFilmXML(id):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    result = session.execute(query.format(module_import, UDF.filmXML.format(str(id))))


    return result