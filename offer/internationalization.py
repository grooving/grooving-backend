spanish = {
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence"
}

english = {
    "ERROR_OFFER_NOT_FOUND": "Offer not found",
    "ERROR_NOT_OFFER_OWNER": "You are not the owner of the offer"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
