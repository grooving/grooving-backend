spanish = {
    "ERROR_PROTFOLIOMODULE_NOT_FOUND": "El módulo del portfolio no existe",
    "ERROR_USER_FORBIDDEN": "El usuario tiene prohibido esta acción",
    "ERROR_FIELD_TYPE": "Campo tipo no rellenado",
    "ERROR_FIELD_LINK": "Campo enlace no rellenado",
    "ERROR_FIELD_DESCRIPTION": "Campo descripción no rellenado",
    "ERROR_FIELD_PORTFOLIO": "Campo portfolio no rellenado",
    "ERROR_NOTFOUND_TYPE": "El tipo no ha sido encontrado",
    "ERROR_NOTVALID_LINK": "El enlace introducido no es válido",
    "ERROR_NOTFOUND_PORTFOLIO": "El portfolio no ha sido encontrado",
    "ERROR_CREATEMODULE_TWITTER": "No puedes crear otro modulo de Twitter",
    "ERROR_CREATEMODULE_INSTAGRAM": "No se puede crear otro modulo de Instagram",
    "ERROR_REFERENCE_PORTFOLIO": "No puedes referenciar este portfolio"
}

english = {
    "ERROR_PROTFOLIOMODULE_NOT_FOUND": "Portfolio module doesn't exist",
    "ERROR_USER_FORBIDDEN": "User has forbidden this action",
    "ERROR_FIELD_TYPE": "Type field hasn't been provided",
    "ERROR_FIELD_LINK": "Link field hasn't been provided",
    "ERROR_FIELD_DESCRIPTION": "Description field hasn't been provided",
    "ERROR_FIELD_PORTFOLIO": "Portfolio field hasn't been provided",
    "ERROR_NOTFOUND_TYPE": "Type isn't exist",
    "ERROR_NOTVALID_LINK": "Link provided isn't valid",
    "ERROR_NOTFOUND_PORTFOLIO": "Portfolio doesn't exist",
    "ERROR_CREATEMODULE_TWITTER": "Can't create another Twitter module",
    "ERROR_CREATEMODULE_INSTAGRAM": "Can't create another Instagram module",
    "ERROR_REFERENCE_PORTFOLIO": "Can't assign this portfolio"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
