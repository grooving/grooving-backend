spanish = {

    "ERROR_VALUE_NULL": "La ID no puede ser nula.",
    "ERROR_OBJECT_NOT_FOUND": "No hay un objeto que corresponda con esta ID.",
    "ERROR_NOT_A_VALID_ID": "La ID introducida no es válida.",
    "ERROR_STRING_TOO_LONG": "La cadena de caracteres es demasiado larga."
}

english = {

    "ERROR_VALUE_NULL": "The ID cannot be null.",
    "ERROR_OBJECT_NOT_FOUND": "The object you are trying to retrieve does not exist.",
    "ERROR_NOT_A_VALID_ID": "The given ID is not valid.",
    "ERROR_STRING_TOO_LONG": "The string is too long"

}


def translate(key_language: str, key_to_translate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[key_language][key_to_translate]}
