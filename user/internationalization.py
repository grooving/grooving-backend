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
    "ERROR_DELETE_USER_UNKNOWN": "User to delete unknown",
    "ERROR_DELETE_USER": "User deletion hasn't been successful",
    "ERROR_USER_FORBIDDEN": "User has forbidden this action",
    "ERROR_FIELD_ID": "Id value hasn't been provided",
    "ERROR_BAN_USER_UNKNOWN": "Ban to user hasn't been successful"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
