from whoosh import index
from whoosh import sorting
from whoosh.qparser import QueryParser, FuzzyTermPlugin, SequencePlugin, PhrasePlugin
from whoosh.query import FuzzyTerm, Regex
from whoosh.query.terms import MultiTerm
from whoosh.sorting import MultiFacet
from utils.whooshSearcher.schemas import crear_esquema
from Grooving.models import Portfolio, Artist
import os
from django.conf import settings
BASE_DIR = settings.BASE_DIR
def search(busqueda="", categoria="", zone="", order=""):

    ix = index.open_dir(os.path.join(BASE_DIR, 'utils/whooshSearcher/index'))
    lista = []
    with ix.searcher() as searcher:
        query = None
        if not busqueda:
            query = QueryParser("artisticName", ix.schema).parse("*")
        else:
            query = querySearchGenerator(busqueda)
            print(query)
        if categoria:
            categoria.replace(" ", "#")
            query = query & queryGenderGenerator(categoria)
        if zone:
            query = query & queryZoneGenerator(zone)
        print(query)
        if order == "asc":
            order = sorting.FieldFacet("rating", reverse=False)
        elif order == "desc":
            order = sorting.FieldFacet("rating", reverse=True)
        else:
            order = sorting.ScoreFacet()

        results = searcher.search(query, sortedby=order, limit=2000)

        for r in results:
            lista.append(r['id'])
            print(r['id'])
        try:
            #query = Artist.objects.filter(portfolio=lista[0]).all()
            #for i in lista[1:0]:
             #   query = query | Artist.objects.filter(portfolio=i).all()
            lista = [Artist.objects.filter(portfolio=i).first() for i in lista]
            #lista =query
        except:
            lista = list(Artist.objects.all())
        return lista


def querySearchGenerator(busqueda):
    trozos = busqueda.split(" ")
    query = None
    print(trozos)

    for p in trozos:
        if query is None:
            query = QueryParser("artisticName", crear_esquema()).parse("*" + p + "*")
            print(query)
        else:
            query = query | QueryParser("artisticName", crear_esquema()).parse("*" + p + "*")


    return query


def queryGenderGenerator(busqueda):
    parser = QueryParser("artisticGender", crear_esquema())
    #parser.remove_plugin_class(PhrasePlugin)
    #parser.add_plugin(SequencePlugin())

    # parser.add_plugin(FuzzyTermPlugin())
    query = parser.parse("*" + busqueda + "*")
    # query = FuzzyTerm("artisticGender", "*"+busqueda+"*", maxdist=int(len(busqueda) / 4))

    return query

def queryZoneGenerator(busqueda):

    parser = QueryParser("zone", crear_esquema())
    query = parser.parse(busqueda)

    return query

# print(listarPorAtributo(nElementosPagina=10,pagina=1))
