spanish = {
    "ERROR_NO_ARTISTIC_NAME": "No has introducido un nombre artistico.",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NOT_AN_ARTIST": "No eres un artista, y por tanto no puedes estar en este sitio.",
    "ERROR_NO_ARTIST_FOUND": "El artista que buscas no existe.",
    "ERROR_OFFER_NOT_OWNED": "Esta oferta no te pertenece.",
    "ERROR_OFFER_NOT_FOUND": "La oferta que buscas no existe.",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_ACTOR_NOT_FOUND": "El actor que buscas no existe.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar."
}

english = {
    "ERROR_NO_ARTISTIC_NAME": "You did not submit an artistic name.",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to do this action.",
    "ERROR_NOT_AN_ARTIST": "You are not an artist, and therefore you cannot be here.",
    "ERROR_NO_ARTIST_FOUND": "The artist you are searching for does not exist.",
    "ERROR_OFFER_NOT_OWNED": "This offer is not yours.",
    "ERROR_OFFER_NOT_FOUND": "The offer you are searching for does not exist.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_MATCHING_LANGUAGE": "The language you want is not available.",
    "ERROR_ACTOR_NOT_FOUND": "The actor you are searching does not exist.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must give a language to switch to."

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
