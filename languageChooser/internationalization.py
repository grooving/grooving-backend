spanish = {
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible."

}

english = {
    "ERROR_NO_GIVEN_LANGUAGE": "You must give a language to switch to.",
    "ERROR_NO_MATCHING_LANGUAGE": "The language you want is not available."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
