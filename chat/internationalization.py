spanish = {
    "DENIED_PEMISSION_CHAT": "No tienes permiso para ver los mensajes."

}

english = {
    "DENIED_PEMISSION_CHAT": "You do not have permission to see messages."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
