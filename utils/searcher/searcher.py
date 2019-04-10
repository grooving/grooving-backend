

from Grooving.models import Portfolio, Rating, Artist
from utils.searcher.distancia import artisticNameCompare, categoriaCompare, zoneCompare

def search(artisticName="", categoria="", zone="", order=""):


    portfolios = Portfolio.objects.all()
    filtersPortfolios = [(porfolio, 0) for porfolio in portfolios if compare(porfolio, artisticName=artisticName,
                                                                   categoria=categoria, zone=zone)]

    rateDict = {}
    for porfolio in filtersPortfolios:
        rateDict.update({porfolio: calculate_rating(porfolio)})

    if order == "asc":
        filtersPortfolios = sorted(rateDict.items(), key=lambda p: p[1], reverse=False)
    if order == "desc":
        filtersPortfolios = sorted(rateDict.items(), key=lambda p: p[1], reverse=True)

    artists = [Artist.objects.filter(portfolio=i[0].id).first() for i in filtersPortfolios]
    return artists


def calculate_rating(portfolio):
    res = 0
    ratings = Rating.objects.filter(offer__paymentPackage__portfolio=portfolio)
    for rating in ratings:
        res += rating.score
    return round(res/len(ratings), ndigits=1) if len(ratings) != 0 else 0.0


def compare(portfolio, artisticName="",categoria="",zone=""):
    coincidencesNeeded = 0
    coincidencesFinded = 0
    if artisticName:
        coincidencesNeeded=coincidencesNeeded+1
        artisticName=artisticName.strip().replace(" ", "#")

        coincidencesFinded = coincidencesFinded + artisticNameCompare(portfolio.artisticName.replace(" ", "#"), artisticName)
    if categoria:
        coincidencesNeeded=coincidencesNeeded+1
        categoria= categoria.strip().replace(" ", "#")
        coincidencesFinded = coincidencesFinded + categoriaCompare(gender_to_string(portfolio), categoria)
    if zone:
        coincidencesNeeded=coincidencesNeeded+1
        zone = zone.strip().replace(" ", "#")
        coincidencesFinded = coincidencesFinded + zoneCompare(zone_to_string(portfolio), zone)

    equals = False
    if coincidencesFinded == coincidencesNeeded:
        equals =True
    return equals


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

