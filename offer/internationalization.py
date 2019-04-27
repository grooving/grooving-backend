spanish = {
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence",
    "ERROR_NO_ARTIST_FOUND": "El artista que buscas no existe.",
    "ERROR_NULL_ARTIST": "Debes especificar el artista que va a introducir el código de pago.",
}

english = {
    "ERROR_OFFER_NOT_FOUND": "Offer not found",
    "ERROR_NOT_OFFER_OWNER": "You are not the owner of the offer",
    "ERROR_NO_ARTIST_FOUND": "The artist you are searching for does not exist.",
    "ERROR_NO_PAYMENTCODE_FOUND": "The artist you are searching for does not exist.",
    "ERROR_NULL_ARTIST": "You must give the artist that will accept the payment code.",
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
