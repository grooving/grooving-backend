spanish = {
    "ERROR_ARTISTIC_GENRE_NOT_FOUND": "Este género artístico no existe",
    "ERROR_INCORRECT_ID": "El ID proporcionado no es válido.",
    "ERROR_NO_PARENT_GENRE_ID": "No se ha proporcionado un id de un género artístico padre válido.",
    "ERROR_GENRE_NULL_NAME": "Debes dar un nombre para el género artístico",
    "ERROR_PARENT_GENRE_NOT_FOUND": "Este género artístico padre no existe",
    "ERROR_IN_CREATION": "Error durante la creacion, intentelos de nuevo",
    "ERROR_GENRE_DOESNT_EXIST": "No existe un genero con esa id",
    "ERROR_GENRE_EXISTS": "Existe un genro con ese nombre",
    "ERROR_NO_USER": "No hay usuarios de este tipo",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NOT_AN_ADMIN": "No eres un administrador, y por tanto no puedes estar en este sitio.",
    "ERROR_OFFER_OF_THIS_KIND": "No hay ofertas de este tipo",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_ONLY_ONE_OPTION": "Se ha seleccionado mas de una opcion de edicion.",
    "ERROR_TREE_OPTION" : "Invalid tree value",
    "ERROR_NO_PORTFOLIO": "Porfolio no existe.",
    "ERROR_STRING_TOO_LONG": "El nombre es demasiado largo.",
    "ERROR_DEEPTH_3":"No puedes crear más de tres niveles."
}

english = {
    "ERROR_STRING_TOO_LONG": "The name is too long",
    "ERROR_INCORRECT_ID": "The given ID is not valid.",
    "ERROR_NO_PARENT_GENRE_ID": "The given parent gender is not valid.",
    "ERROR_GENRE_NULL_NAME": "You must provide a name for the genre.",
    "ERROR_ARTISTIC_GENRE_NOT_FOUND": "Este género artístico no existe",
    "ERROR_IN_CREATION": "Error during the creation, try again",
    "ERROR_GENRE_DOESNT_EXIST": "A parent Genre doesnt exist with that id",
    "ERROR_PARENT_GENRE_NOT_FOUND": "This parent genre does not exist.",
    "ERROR_GENRE_EXISTS": "A Genre with that name already exists",
    "ERROR_NO_USER": "There are no users of this type",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_NOT_AN_ADMIN": "You are not an administrador, so you cannot be here.",
    "ERROR_OFFER_OF_THIS_KIND": "There are no offers of this kind.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_MATCHING_LANGUAGE": "This language is not available.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must choose a language.",
    "ERROR_ONLY_ONE_OPTION": "More than one edition option given.",
    "ERROR_TREE_OPTION" : "Error en el valor de tree",
    "ERROR_NO_PORTFOLIO": "Porfolio does not exist.",
    "ERROR_DEEPTH_3": "More than 3 levels can not be create."

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
