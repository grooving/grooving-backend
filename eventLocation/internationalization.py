spanish = {
    "ERROR_CUSTOMER_NOT_FOUND": "No eres un cliente",
    "ERROR_ADDRESS_NOT_PROVIDED": "No has introducido la dirección",
    "ERROR_ZONE_NOT_PROVIDED": "No has introducido una zona",
    "ERROR_ZONE_NOT_FOUND": "No existe la zona introducida",
    "ERROR_ZONE_CAN_NOT_ASSIGNED": "Esta zona no puede ser asignada",
    "ERROR_NAME_TOO_LONG": "El nombre de la ciudad es demasiado largo.",
    "ERROR_ADDRESS_TOO_LONG": "La dirección es demasiado larga."
}

english = {
    "ERROR_NAME_TOO_LONG": "The town name is too long.",
    "ERROR_ADDRESS_TOO_LONG": "The address is too long.",
    "ERROR_CUSTOMER_NOT_FOUND": "You aren't an customer user",
    "ERROR_ADDRESS_NOT_PROVIDED": "You haven't provided an address",
    "ERROR_ZONE_NOT_PROVIDED": "You haven't provided a valid zone",
    "ERROR_ZONE_NOT_FOUND": "Zone provided hasn't been found",
    "ERROR_ZONE_CAN_NOT_ASSIGNED": "This zone can't be assigned"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
