from imdb import IMDb
from lxml import etree
import os, sys
from lib import querys
from BaseXClient import BaseXClient


badTags = ["editorial-department","make-up-department","assistant-directors","art-department","sound-department","special-effects","visual-effects","stunts","camera-department","animation-department","casting-department","costume-departmen","location-management","music-department","script-department","transportation-department","miscellaneous","akas","special-effects-companies","other-companies"]


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
    temp = open(str(querys.BASE_DIR) + "/querys/temp.xml", 'wb')
    temp.write(xml)
    temp.close()
    session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
    q = querys.query.format(querys.module_import, querys.UDF.insertFilm.format("'" + str(querys.BASE_DIR) + "/querys/temp.xml" + "'", "'" + id + "'"))

    result = session.execute(q)

    os.remove(str(querys.BASE_DIR) + "/querys/temp.xml")


def validate(xml, schemaUrl):

    schema = open(str(querys.BASE_DIR) + schemaUrl, 'rb')
    schema = etree.fromstring(schema.read())
    schema = etree.XMLSchema(schema)
    parser = etree.XMLParser(schema=schema)

    validatedXML = etree.fromstring(xml, parser)