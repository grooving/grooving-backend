spanish = {
    "ERROR_NO_USER": "No hay usuarios de este tipo",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NOT_AN_ADMIN": "No eres un administrador, y por tanto no puedes estar en este sitio.",
    "ERROR_OFFER_OF_THIS_KIND": "No hay ofertas de este tipo",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar."
}

english = {
    "ERROR_NO_USER": "There are no users of this type",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_NOT_AN_ADMIN": "You are not an administrador, so you cannot be here.",
    "ERROR_OFFER_OF_THIS_KIND": "There are no offers of this kind.",
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