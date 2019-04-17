

from Grooving.models import Portfolio, Rating, Artist, Customer
from utils.searcher.distancia import artisticNameCompare, categoriaCompare, zoneCompare

def searchAdmin(userName=""):
    artists = Artist.objects.all()
    filterArtists = [artist for artist in artists if compare(artist, userName)]
    customers = Customer.objects.all()
    filterCustomers = [customer for customer in customers if compare(customer, userName)]

    return {"artists": filterArtists, "customers": filterCustomers}

def compareUsers(user, userName=""):
    coincidencesNeeded = 0
    coincidencesFinded = 0
    if userName:
        coincidencesNeeded = 1
        userName = userName.strip().replace(" ", "#")
        coincidencesFinded = artisticNameCompare(user.username.replace(" ", "#"), userName)

    equals = False

    if coincidencesFinded == coincidencesNeeded:
        equals = True

    return equals


def search(artisticName="", categoria="", zone="", order=""):


    portfolios = Portfolio.objects.all()
    filtersPortfolios = [(porfolio, 0) for porfolio in portfolios if compare(porfolio, artisticName=artisticName,
                                                                   categoria=categoria, zone=zone)]

    rateDict = {}
    for portfolio in filtersPortfolios:
        rateDict.update({portfolio[0]: portfolio[0].artist.rating})

    if order == "asc":
        filtersPortfolios = sorted(rateDict.items(), key=lambda p: p[1], reverse=False)
    if order == "desc":
        filtersPortfolios = sorted(rateDict.items(), key=lambda p: p[1], reverse=True)

    artists = [Artist.objects.filter(portfolio=i[0].id).first() for i in filtersPortfolios]
    return artists


def compare(portfolio, artisticName="", categoria="", zone=""):
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
    all_child = get_parents_gender(genders)
    string = array_to_string(all_child)
    return string


def zone_to_string(portfolio):
    zones = portfolio.zone.all()
    all_childs = get_childs_zone(zones, [])
    all_parents = get_parents_zone(zones)
    string = array_to_string(all_childs) + array_to_string(all_parents)
    return string


def get_parents_gender(genders):
    parent_gender = []
    genders = list(genders)
    for gender in genders:
        parent = gender.parentGender
        while parent is not None:
            if parent not in parent_gender:
                genders.append(parent)
                parent = parent.parentGender
    return genders


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

