spanish = {
    "ERROR_ADMIN_NOT_FOUND": "No eres un administrador",
    "ERROR_SUBJECT_NOT_PROVIDED": "No has introducido el asunto",
    "ERROR_BODY_NOT_PROVIDED": "No has introducido el cuerpo",
}

english = {
    "ERROR_ADMIN_NOT_FOUND": "You aren't an admin user",
    "ERROR_SUBJECT_NOT_PROVIDED": "Subject field not provided",
    "ERROR_BODY_NOT_PROVIDED": "Body field not provided",
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
