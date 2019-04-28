spanish = {
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_OFFER_NOT_OWNED": "Esta oferta no te pertenece.",
    "USER_DELETED_DATA": "Esta oferta ha sido cancelada porque el usuario ha borrado sus datos de la aplicación.",
    "ERROR_NOT_AN_ARTIST": "No eres un artista",
    "ERROR_NO_ARTIST_FOUND": "Artista no encontrado",
    "ERROR_NOT_A_CUSTOMER": "No eres un cliente",
}

english = {
    "ERROR_OFFER_NOT_FOUND": "Offer not found",
    "ERROR_NOT_OFFER_OWNER": "You are not the owner of the offer",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to do this action.",
    "ERROR_OFFER_NOT_OWNED": "This offer is not yours.",
    "USER_DELETED_DATA": "This offer is cancelled because the user deleted their data.",
    "ERROR_NOT_AN_ARTIST": "You are not an artist.",
    "ERROR_NO_ARTIST_FOUND": "Artist not found",
    "ERROR_NOT_A_CUSTOMER": "You are not a customer",

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
