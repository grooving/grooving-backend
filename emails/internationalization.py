spanish = {
    "ERROR_ADMIN_NOT_FOUND": "No eres un administrador",
    "ERROR_SUBJECT_NOT_PROVIDED": "No has introducido el asunto",
    "ERROR_BODY_NOT_PROVIDED": "No has introducido el cuerpo",
    "ERROR_USER_NOT_FOUND": "No eres artista o cliente",
    "ERROR_SUBJECT_CANT_BE_INTEGER": "El asunto no puede ser entero.",
    "ERROR_BODY_CANT_BE_INTEGER": "El cuerpo no puede ser entero."
}

english = {
    "ERROR_ADMIN_NOT_FOUND": "You aren't an admin user",
    "ERROR_SUBJECT_NOT_PROVIDED": "Subject field not provided",
    "ERROR_BODY_NOT_PROVIDED": "Body field not provided",
    "ERROR_USER_NOT_FOUND": "You aren't an artist or customer user",
    "ERROR_SUBJECT_CANT_BE_INTEGER": "Subject can't be integer.",
    "ERROR_BODY_CANT_BE_INTEGER": "Body can't be integer."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
