import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Server.settings')
django.setup()
from whoosh import index
from whoosh import sorting
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from whoosh.query import FuzzyTerm, Regex
from whoosh.query.terms import MultiTerm
from whoosh.sorting import MultiFacet
from utils.whooshSearcher.schemas import crear_esquema





def listarPorAtributo(busqueda="", categoria="", zone="", order=""):
    tam = 0
    ix = index.open_dir("index")
    lista = []
    busqueda = busqueda.strip()
    with ix.searcher() as searcher:
        #if (not (busqueda) and not (categoria)):
        #    query = QueryParser("artisticName", ix.schema).parse("*")
        #elif (not (busqueda) and categoria):
        #    query = QueryParser("artisticName", ix.schema).parse("*") & queryCategoryGenerator(categoria)
        #elif (busqueda and not (categoria)):
        #    query = querySearchGenerator(busqueda)
        #elif (busqueda and categoria):
        #    query = querySearchGenerator(busqueda) & queryCategoryGenerator(categoria)
        query = queryGenderGenerator("oc")
        query.normalize()
        if order == "+":
            order = sorting.FieldFacet("rating", reverse=False)
        elif order == "-":
            order = sorting.FieldFacet("rating", reverser=True)
        else:
            order = sorting.ScoreFacet()


        results = searcher.search(query, sortedby=order, limit=4000)

        for r in results:
            lista.append(r['id'])
        return lista


def querySearchGenerator(busqueda):
    trozos = busqueda.split(" ")
    query = None
    for p in trozos:
        if (query is None):
            query = FuzzyTerm("artisticName", p, maxdist=int(len(p) / 4))
        else:
            query = query | FuzzyTerm("artisticName", p, maxdist=int(len(p) / 4))
    return query


def queryGenderGenerator(busqueda):
    parser = QueryParser("artisticGender", crear_esquema())
    parser.add_plugin(FuzzyTermPlugin())
    query = parser.parse("*"+busqueda+"~"+str(int(len("busqueda")/4))+"*")


    return query

def queryZoneGenerator(busqueda):

    parser = QueryParser("zone", crear_esquema())
    query = parser.parse()

    return query

# print(listarPorAtributo(nElementosPagina=10,pagina=1))

print(listarPorAtributo())