
from _decimal import Decimal
import os
import django
django.setup()
from django.core.paginator import Paginator
from whoosh import index
from Grooving.models import Portfolio
from utils.whooshSearcher.schemas import crear_esquema

def index_all():
    if not os.path.exists("index"):
        os.mkdir("index")
    index.create_in("index", crear_esquema())

    ix = index.open_dir("index")


    writer = ix.writer()
    portfolios = Portfolio.objects.all().order_by("id")

    paginator = Paginator(portfolios, 20)

    portfolios = paginator.page(1)

    while portfolios.has_next():
        for portfolio in portfolios:
            id = portfolio.id
            artisticName = portfolio.artisticName
            biography = portfolio.biography
            artisticGender = portfolio.artisticGender # TODO: añadir hijos.
            zone = portfolio.zone # TODO: añadir hijos.
            rating= get_media()

            writer.add_document(id=id, artisticName=artisticName, biography=biography,
                                artisticGender=artisticGender, zone=zone)

        portfolios = paginator.page(portfolios.next_page_number())
    writer.commit()


def get_media():
    return 2.5

def gender_to_string(portfolio):



