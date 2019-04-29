spanish = {
    "ERROR_INCORRECT_ID": "El ID proporcionado no es válido.",
    "ERROR_IN_CREATION": "Error durante la creacion, intentelos de nuevo",
    "ERROR_GENRE_DOESNT_EXIST": "No existe un genero con esa id",
    "ERROR_ZONE_DOESNT_EXIST": "No existe una zona con esa id",
    "ERROR_NO_USER": "No hay usuarios de este tipo",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_NO_PORTFOLIO": "Porfolio no existe.",
    "ERROR_NO_PORTFOLIO_USER": "Porfolio no es de este usuario."
}

english = {

    "ERROR_INCORRECT_ID": "The given ID is not valid.",
    "ERROR_IN_CREATION": "Error during the creation, try again",
    "ERROR_GENRE_DOESNT_EXIST": "A Genre doesnt exist with that id",
    "ERROR_ZONE_DOESNT_EXIST": "A  Zone doesnt exist with that id",
    "ERROR_NO_USER": "There are no users of this type",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_MATCHING_LANGUAGE": "This language is not available.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must choose a language.",
    "ERROR_NO_PORTFOLIO": "Porfolio does not exist.",
    "ERROR_NO_PORTFOLIO_USER": "Porfolio not from this user.",
    "ERROR_ARTISTIC_NAME": 'Artistic Name must be a string',
    "ERROR_BANNER_STRING" : 'Banner must be a string',
    "ERROR_BANNER_URL" : 'Invalid banner url,the banner must start with http',
    "ERROR_BANNER_FORMAT" : "Invalid image format banner.",
    "ERROR_BIOGRAPHY_STRING" : 'Biography must be a string',
    "ERROR_IMAGE_STRING" : 'Image must be a string',
    "ERROR_IMAGE_URL" : 'Invalid Image url,the Image must start with http',
    "ERROR_IMAGE_FORMAT" : "Invalid image format.",
    "ERROR_VIDEO_FORMAT" : "Invalid video format, the video must be from youtube",
    "ERROR_VIDEO_STRING" : 'Video must be a string',
    "ERROR_PHOTO_STRING" : 'Main photo must be a string',
    "ERROR_PHOTO_URL" : 'Invalid main photo url,the Image must start with http',
    "ERROR_PHOTO_FORMAT" : "Invalid main photo format."


}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
