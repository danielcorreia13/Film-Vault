import xmltodict
from pathlib import Path
from imdb import IMDb
from lxml import etree
import os
from BaseXClient import BaseXClient
from django.conf import settings



badTags = ["editorial-department","make-up-department","assistant-directors","art-department","sound-department","special-effects","visual-effects","stunts","camera-department","animation-department","casting-department","costume-departmen","location-management","music-department","script-department","transportation-department","miscellaneous","akas","special-effects-companies","other-companies"]



BASE_DIR = settings.BASE_DIR


class UDF():
    filmsByYear = "funcs:filmsOrderByYearPage({}, {}, {} {})"
    filmsByAlfa = "funcs:filmsOrderByAlfaPage({}, {}, {} {})"
    filmXML     = "funcs:getFilm({})"
    insertFilm  = "funcs:newFilm({}, {})"

module_import = "import module namespace funcs = 'funcs' at '" + str(BASE_DIR) + "/querys/funcs.xq'; \n "
query = "xquery {} {}"

def executeQuery(funcSrt, pageIndex, n, syear = None, fyear = None, cat = '', search = ''):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    pageIndex -= 1
    search = "'{}'".format(search)
    cat = "'{}'".format(cat)
    if not cat is None and cat != "''":
        if syear != None and fyear != None:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ", {}, {}, {}".format(syear, fyear, cat)))
        else:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ", {}".format(cat)))
    else:
        if syear != None and fyear != None:
            q = query.format(module_import, funcSrt.format(search, pageIndex, n, ", {}, {}".format(syear, fyear)))
        else:

            q = query.format(module_import, funcSrt.format(search, pageIndex, n, " "))
    print(q)
    result = session.execute(q)
    dict = xmltodict.parse(result)
    if not dict['root']:
        return None
    return [movie for movie in dict['root']['elem']]

def getFilmsSortedByYear(pageIndex, n, syear = None, fyear = None, cat = '', search = ""):
    return executeQuery(UDF.filmsByYear, pageIndex, n, syear, fyear, cat, search)

def getFilmsSortedByAlfa(pageIndex, n, syear = None, fyear = None, cat = '', search = ""):
    return executeQuery(UDF.filmsByAlfa, pageIndex, n, syear, fyear, cat, search)

def getFilmXML(id):
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')

    result = session.execute(query.format(module_import, UDF.filmXML.format(str(id))))


    return result

def newFilm(id):
    print(id)
    ia = IMDb('https')
    movie = ia.get_movie(str(id))
    xml = movie.asXML(_with_add_keys=False)
    tree = etree.fromstring(xml)
    for elem in tree:
        tag = elem.tag
        if tag in badTags:
            tree.remove(elem)
    xml = etree.tostring(tree)
    try:
        validate(xml, "/xml/movie.xsd")
    except Exception as e:
        print("XML not valid")
        print(e)
        return
    temp = open(str(BASE_DIR) + "/querys/temp.xml", 'wb')
    temp.write(xml)
    temp.close()
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    q = query.format(module_import, UDF.insertFilm.format("'" + str(
        BASE_DIR) + "/querys/temp.xml" + "'", "'" + id + "'"))

    result = session.execute(q)

    os.remove(str(BASE_DIR) + "/querys/temp.xml")


def validate(xml, schemaUrl):

    schema = open(str(BASE_DIR) + schemaUrl, 'rb')
    schema = etree.fromstring(schema.read())
    schema = etree.XMLSchema(schema)
    parser = etree.XMLParser(schema=schema)

    validatedXML = etree.fromstring(xml, parser)


