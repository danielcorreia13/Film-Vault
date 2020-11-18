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

badTags = ["editorial-department","make-up-department","assistant-directors","art-department","sound-department","special-effects","visual-effects","stunts","camera-department","animation-department","casting-department","costume-departmen","location-management","music-department","script-department","transportation-department","miscellaneous","akas","special-effects-companies","other-companies"]

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
    q = query.format(module_import, UDF.insertFilm.format("'" + str(BASE_DIR) + "/querys/temp.xml" + "'", "'" + id + "'"))

    result = session.execute(q)

    os.remove(str(BASE_DIR) + "/querys/temp.xml")

def test():
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    q = query.format(module_import, "let $films := collection('Films')//movie\n" +
                                    "for $film in $films\n" +
                                    "return $film")
    result = session.execute(q)
    result = result.split("</movie>")

    schema = open(str(BASE_DIR) + "/xml/movie.xsd", 'rb')
    schema = etree.fromstring(schema.read())
    schema = etree.XMLSchema(schema)
    parser = etree.XMLParser(schema=schema)

    for xml in result:
        if xml == "":
            return
        xml += "</movie>"
        tree = etree.fromstring(xml)
        try:
            validatedXML = etree.fromstring(xml, parser)
            print("nice")
        except Exception as e:
            print(xml)
            print(e)
            exit(1)



def validate(xml, schemaUrl):

    schema = open(str(BASE_DIR) + schemaUrl, 'rb')
    schema = etree.fromstring(schema.read())
    schema = etree.XMLSchema(schema)
    parser = etree.XMLParser(schema=schema)

    validatedXML = etree.fromstring(xml, parser)


for i in getFilmsSortedByAlfa(1,20,syear=1920, fyear=2017, cat="Adventure",search="Harry"):
    print(i['title'])
    print("\n")

# print(getFilmXML('0948470'))

# newFilm("9695722")
#
# newFilm("8337320")
