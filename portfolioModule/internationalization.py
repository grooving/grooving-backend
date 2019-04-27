spanish = {
    "ERROR_NO_ARTISTIC_NAME": "No has introducido un nombre artistico.",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NOT_AN_ARTIST": "No eres un artista, y por tanto no puedes estar en este sitio.",
    "ERROR_NO_ARTIST_FOUND": "El artista que buscas no existe.",
    "ERROR_OFFER_NOT_OWNED": "Esta oferta no te pertenece.",
    "ERROR_OFFER_NOT_FOUND": "La oferta que buscas no existe.",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_INVALID_PARAMETERS": "Los parámetros dados en la petición no son válidos",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_ACTOR_NOT_FOUND": "El actor que buscas no existe.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_PORTFOLIOMODULE_NOT_FOUND": "Este módulo de portfolio no existe.",
    "ERROR_FIELD_TYPE": "Debes indicar el tipo de módulo.",
    "ERROR_FIELD_LINK": "Debes indicar un enlace.",
    "ERROR_FIELD_DESCRIPTION": "Debes indicar una descripción.",
    "ERROR_FIELD_PORTFOLIO": "Debes indicar un portfolio al que asociar este módulo.",
    "ERROR_NOTFOUND_TYPE": "Este tipo de módulo no existe.",
    "ERROR_NOTVALID_LINK": "Este enlace no es válido.",
    "ERROR_NOTFOUND_PORTFOLIO": "Este portfolio no existe",
    "ERROR_CREATEMODULE_TWITTER": "No se ha proporcionado un módulo de Twitter",
    "ERROR_CREATEMODULE_INSTAGRAM": "No se ha dado un módulo de Instagram.",
    "ERROR_REFERENCE_PORTFOLIO": "No eres el dueño de este portfolio."

}

english = {
    "ERROR_NO_ARTISTIC_NAME": "You did not submit an artistic name.",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to do this action.",
    "ERROR_NOT_AN_ARTIST": "You are not an artist, and therefore you cannot be here.",
    "ERROR_NO_ARTIST_FOUND": "The artist you are searching for does not exist.",
    "ERROR_OFFER_NOT_OWNED": "This offer is not yours.",
    "ERROR_OFFER_NOT_FOUND": "The offer you are searching for does not exist.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_INVALID_PARAMETERS": "The given parameters are not valid.",
    "ERROR_NO_MATCHING_LANGUAGE": "The language you want is not available.",
    "ERROR_ACTOR_NOT_FOUND": "The actor you are searching does not exist.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must give a language to switch to.",
    "ERROR_PORTFOLIOMODULE_NOT_FOUND": "This portfolio module does not exist.",
    "ERROR_FIELD_TYPE": "You must provide a field type.",
    "ERROR_FIELD_LINK": "You must provide a link.",
    "ERROR_FIELD_DESCRIPTION": "You must provide a description.",
    "ERROR_FIELD_PORTFOLIO": "You must provide a portfolio.",
    "ERROR_NOTFOUND_TYPE": "This module type is not supported.",
    "ERROR_NOTVALID_LINK": "this link is not valid. Make sure it belongs to the corresponding website.",
    "ERROR_NOTFOUND_PORTFOLIO": "This portfolio does not exist.",
    "ERROR_CREATEMODULE_TWITTER": "You must provide an Twitter module",
    "ERROR_CREATEMODULE_INSTAGRAM": "You must provide an Instagram module.",
    "ERROR_REFERENCE_PORTFOLIO": "You are not the owner of this portfolio."

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
