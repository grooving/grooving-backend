spanish = {
    "ERROR_NO_USER": "No hay usuarios de este tipo",
    "ERROR_NOT_ALLOWED_USER": "No tienes los privilegios para ver esta página o realizar esta acción.",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence",
    "ERROR_NOT_A_CUSTOMER": "No eres un cliente, y por tanto no puedes estar en este sitio.",
    "ERROR_NOT_AN_ARTIST": "No eres un artista, y por tanto no puedes estar en este sitio.",
    "ERROR_NO_ARTIST_FOUND": "El artista que buscas no existe.",
    "ERROR_NULL_ARTIST": "Debes especificar el artista que va a introducir el código de pago.",
    "ERROR_NO_PAYMENTCODE_FOUND": "No se pudo encontrar el código de pago que buscas.",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar."
}

english = {
    "ERROR_NO_USER": "There are no users of this type",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_OFFER_NOT_FOUND": "Offer not found",
    "ERROR_NOT_AN_ARTIST": "You are not an artist, and therefore you cannot be here.",
    "ERROR_NOT_OFFER_OWNER": "You are not the owner of the offer",
    "ERROR_NOT_A_CUSTOMER": "You are not a customer, and therefore you cannot be here.",
    "ERROR_NO_ARTIST_FOUND": "The artist you are searching for does not exist.",
    "ERROR_NO_PAYMENTCODE_FOUND": "The payment code could not be found.",
    "ERROR_NULL_ARTIST": "You must give the artist that will accept the payment code.",
    "ERROR_NOT_ALLOWED_USER": "You lack the privileges to view this page or perform this action.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_MATCHING_LANGUAGE": "This language is not available.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must choose a language."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
