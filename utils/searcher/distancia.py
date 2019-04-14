from distance import levenshtein


def artisticNameCompare(porfolioArtisticName, searchArtisticName):
    porfolioArtisticName = format(porfolioArtisticName)
    searchArtisticName = format(searchArtisticName)
    contains =searchArtisticName in porfolioArtisticName
    inDistance = isWordInLevenshteinDistance([porfolioArtisticName, ], searchArtisticName)
    equal = 0
    if contains or inDistance:
        equal = 1

    return equal

def categoriaCompare(portfolioCategoria, searchCategoria):
    portfolioCategoria = format(portfolioCategoria)
    searchCategoria = format(searchCategoria)
    contains = searchCategoria in portfolioCategoria
    inDistance = isWordInLevenshteinDistance(portfolioCategoria.split(" "), searchCategoria)
    equal = 0
    if contains or inDistance:
        equal = 1

    return equal

def zoneCompare(portfolioZone, searchZone):
    portfolioZone = format(portfolioZone)
    searchZone = format(searchZone)
    contains = searchZone in portfolioZone
    equal = 0
    if contains:
        equal = 1

    return equal


def getLevenshteinDistance(word1, word2):
    return levenshtein(word1, word2)


def isWordInLevenshteinDistance(list, word):

    isWordInDistance = False
    for listWord in list:
        admisibleDistance = len(listWord.replace("#", "")) / 4
        distance = getLevenshteinDistance(listWord, word)
        if distance <= admisibleDistance:
            isWordInDistance = True
            break
    return isWordInDistance


def format(palabra):
    palabra=palabra.lower().replace("ú", "u").replace("ó", "o").replace("í", "i").replace("é", "e").replace("á", "a")
    return palabra