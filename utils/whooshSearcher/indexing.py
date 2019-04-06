from _decimal import Decimal
import os
import django
import random
import string
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Server.settings')
django.setup()
from django.core.paginator import Paginator
from whoosh import index
from Grooving.models import Portfolio
from utils.whooshSearcher.schemas import crear_esquema
from zone.serializers import SearchZoneSerializer

def index_all():
    if not os.path.exists("utils/whooshSearcher/index"):
        os.mkdir("utils/whooshSearcher/index")
    index.create_in("utils/whooshSearcher/index", crear_esquema())

    ix = index.open_dir("utils/whooshSearcher/index")
    writer = ix.writer()

    portfolios = Portfolio.objects.all().order_by("id")

    for portfolio in portfolios:
        id = portfolio.id
        artisticName = portfolio.artisticName.lower()
        biography = portfolio.biography.lower()
        artisticGender = gender_to_string(portfolio)
        zone = zone_to_string(portfolio)
        rating= portfolio.artist.rating

        writer.add_document(id=id, artisticName=artisticName, biography=biography,
                            artisticGender=artisticGender, zone=zone, rating=rating)


    writer.commit()


def add_update_index_rating(portfolio):
    ix = index.open_dir("index")
    writer = ix.writer()
    id = portfolio.id
    artisticName = portfolio.artisticName.lower()
    biography = portfolio.biography.lower()
    artisticGender = gender_to_string(portfolio)
    zone = zone_to_string(portfolio)
    rating = portfolio.artist.rating
    writer.update_document(id=id, artisticName=artisticName, biography=biography,
                        artisticGender=artisticGender, zone=zone, rating=rating)
    writer.commit()
#def add_update_index_()

def gender_to_string(portfolio):
    genders = portfolio.artisticGender.all()
    all_child = get_childs_gender(genders, [])
    string = array_to_string(all_child)
    return string


def zone_to_string(portfolio):
    zones = portfolio.zone.all()
    all_childs = get_childs_zone(zones, [])
    all_parents = get_parents_zone(zones)
    string = array_to_string(all_childs) + array_to_string(all_parents)
    return string


def get_childs_gender(queryset, total=[]):
    total = total
    for gender in queryset:
        if gender not in total:
            total.append(gender)
            child_genders = gender.artisticgender_set.all()
            total = get_childs_gender(child_genders, total)
    return total


def get_parents_zone(zones):
    parent_zones = []
    zones = list(zones)
    for zone in zones:
        parent = zone.parentZone
        while parent is not None:
            if parent not in parent_zones:
                zones.append(parent)
                parent = parent.parentZone
    return zones


def get_childs_zone(queryset, total=[]):
    total = total
    for zone in queryset:
        if zone not in total:
            total.append(zone)
            child_zone = zone.zone_set.all()
            total = get_childs_zone(child_zone, total)
    return total


def array_to_string(array):
    result = ""
    for a in array:
        result = result + " " +str(a.name.replace(" ", "#").lower())

    return result

def array_of_id_to_string(array):
    result = ""
    for a in array:
        result = result + " " +str(a.id)

    return result

#index_all()

