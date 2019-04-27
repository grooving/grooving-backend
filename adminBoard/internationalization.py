spanish = {
    "ERROR_NO_USER": "No hay usuarios de este tipo",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NOT_AN_ADMIN": "No eres un administrador, y por tanto no puedes estar en este sitio.",
    "ERROR_OFFER_OF_THIS_KIND": "No hay ofertas de este tipo",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_ZONE_NOT_FOUND": "La zona no existe.",
    "ERROR_EMPTY_FORM_NOT_VALID": "El formulario no puede estar vacío.",
    "ERROR_FORBIDDEN_NO_ADMIN": "No tienes permisos para realizar esta acción.",
    "ERROR_ZONE_NAME_NOT_PROVIDED": "Nombre de la zona no indicado.",
    "ERROR_PARENT_ZONE_NOT_PROVIDED": "Zona padre no indicada.",
    "ERROR_ZONE_NAME_TOO_SHORT": "Nombre de la zona demasiado corto",
    "ERROR_ZONE_ALREADY_EXISTS": "La zona introducida ya existe",
    "ERROR_PARENT_ZONE_DOES_NOT_EXIST": "La zona padre no existe",
    "ERROR_ZONE_BELONGS_TO_EVENT":"La zona pertenece a la localización de un artista del sistema,no puede ser borrada"
}

english = {
    "ERROR_NO_USER": "There are no users of this type",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_NOT_AN_ADMIN": "You are not an administrador, so you cannot be here.",
    "ERROR_OFFER_OF_THIS_KIND": "There are no offers of this kind.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_MATCHING_LANGUAGE": "This language is not available.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must choose a language.",
    "ERROR_ZONE_NOT_FOUND": "Zone does not exist.",
    "ERROR_EMPTY_FORM_NOT_VALID": "Empty form is not valid.",
    "ERROR_FORBIDDEN_NO_ADMIN": "You don't have permissions to perform this action.",
    "ERROR_ZONE_NAME_NOT_PROVIDED": "Zone name not provided",
    "ERROR_PARENT_ZONE_NOT_PROVIDED": "Parent zone not provided.",
    "ERROR_ZONE_NAME_TOO_SHORT": "Zone name is too short",
    "ERROR_ZONE_ALREADY_EXISTS": "Zone name already exists",
    "ERROR_PARENT_ZONE_DOES_NOT_EXIST": "Parent zone does not exists",
    "ERROR_ZONE_BELONGS_TO_EVENT":"Zone belongs to an artist event location, it cannot be deleted"

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
