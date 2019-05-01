spanish = {
    "ERROR_ZONE_NOT_FOUND": "Zona no encontrada",
    "ERROR_ZONE_NOT_OWNER": "No tienes permisos para modificar esta zona",
    "ERROR_ZONE_NOT_3_OPTION": "La zona no tiene 3 opciones",
    "ERROR_INCORRECT_ID": "Id incorrecto",
    "ERROR_PARENT_ZONE_NOT_FOUND": "Zona padre no encontrada",
    "ERROR_PORTFOLIO_NOT_FOUND": "Porfolio no encontrado",
}

english = {
    "ERROR_ZONE_NOT_FOUND": "Zone not found.",
    "ERROR_ZONE_NOT_OWNER": "You don't have permissions to edit this zone",
    "ERROR_ZONE_NOT_3_OPTION": "Portfolio's zones don't have tree option",
    "ERROR_INCORRECT_ID": "Incorrect id",
    "ERROR_PARENT_ZONE_NOT_FOUND": "Parent zone not found",
    "ERROR_PORTFOLIO_NOT_FOUND": "Porfolio not found",
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
