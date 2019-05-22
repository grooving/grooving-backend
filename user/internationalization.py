spanish = {
    "ERROR_VALIDATE": "La validación de los datos ha sido erronea",
    "ERROR_DELETE_USER_UNKNOWN": "Error al eliminar un usuario desconocido",
    "ERROR_DELETE_USER": "Error al eliminar usuario",
    "ERROR_USER_FORBIDDEN": "El usuario tiene prohibido esta acción",
    "ERROR_FIELD_ID": "Campo id no rellenado",
    "ERROR_BAN_USER_UNKNOWN": "Error al banear un usuario desconocido"
}

english = {
    "ERROR_VALIDATE": "Data validation hasn't been successful",
    "ERROR_DELETE_USER_UNKNOWN": "The user you try to delete does not exist",
    "ERROR_DELETE_USER": "The user data could not be deleted",
    "ERROR_USER_FORBIDDEN": "You can't perform this action",
    "ERROR_FIELD_ID": "Id value not provided provided",
    "ERROR_BAN_USER_UNKNOWN": "There was a problem banning this user"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
