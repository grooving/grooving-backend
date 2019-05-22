spanish = {
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en esta zona."

}

english = {
    "ERROR_NO_GIVEN_LANGUAGE": "You must give a language to switch to.",
    "ERROR_NO_MATCHING_LANGUAGE": "The language you want is not available.",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to do this action."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
