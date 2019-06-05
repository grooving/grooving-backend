spanish = {
    "ERROR_PORTFOLIO_NOT_FOUND": "El portfolio no existe",
    "ERROR_NOT_LOGGED_OR_NOT_OWNER": "No tienes permiso para modificar este portfolio",
    "ERROR_ARTISTICNAME_BAD_PROVIDED": "El nombre artístico introducido no es válido",
    "ERROR_BIOGRAPHY_BAD_PROVIDED": "La biografía introducida no es válida",
    "ERROR_BANNER_BAD_PROVIDED": "El banner introducido no es válido",
    "ERROR_BANNER_NOT_VALID_URL": "La URL del banner no es valida",
    "ERROR_BANNER_NOT_URL_IMAGE": "La URL del banner no es una imagen",
    "ERROR_IMAGE_BAD_PROVIDED": "La imagen introducida no es válida",
    "ERROR_IMAGE_NOT_VALID_URL": "La URL de la imagen no es válida",
    "ERROR_IMAGE_NOT_URL_IMAGE": "La URL de la imagen no es una imagen",
    "ERROR_VIDEO_YOUTUBE": "El video no es de YouTube",
    "ERROR_VIDEO_BAD_PROVIDED": "El video introducido no es válido",
    "ERROR_GENRE_NOT_FOUND": "El género artístico no existe",
    "ERROR_ZONE_NOT_FOUND": "La zona no existe",
    "ERROR_MAINPHOTO_BAD_PROVIDED": "La foto principal introducida no es válida",
    "ERROR_MAINPHOTO_NOT_VALID_URL": "La URL de la foto principal no es válida",
    "ERROR_MAINPHOTO_NOT_URL_IMAGE": "La URL de la foto principal no es una imagen",
    "ERROR_STRING_TOO_LONG": "La cadena de caracteres es demasiado larga.",
    "ERROR_URL_TOO_LONG": "La URL es demasiado larga. El límite es 500 caracteres.",
    "ERROR_BIOGRAPHY_TOO_LONG": "La biografía es demasiado larga.",
    "ERROR_ARTISTICNAME_TOO_LONG": "El nombre artístico es demasiado largo.",
    "ERROR_VIDEO_URL_TOO_LONG": "La URL del vídeo es demasiado larga",
    "ERROR_IMAGE_URL_TOO_LONG": "La URL de la imagen es demasiado larga",
    "ERROR_EMPTY_BIOGRAPHY": "La biografía no puede estar vacía.",
    "ERROR_PORTFOLIO_NOT_OWNER": "No tienes permiso para editar este portfolio"


}

english = {
    "ERROR_EMPTY_BIOGRAPHY": "The biography can't be empty.",
    "ERROR_VIDEO_URL_TOO_LONG": "Video URL is too long.",
    "ERROR_IMAGE_URL_TOO_LONG": "Image URL is too long",
    "ERROR_BIOGRAPHY_TOO_LONG": "The biography is too long.",
    "ERROR_ARTISTICNAME_TOO_LONG": "The artistic name is too long.",
    "ERROR_URL_TOO_LONG": "The URL is too long. Limit is 500 characters.",
    "ERROR_STRING_TOO_LONG": "The string is too long",
    "ERROR_PORTFOLIO_NOT_FOUND": "This portfolio doesn't exist",
    "ERROR_NOT_LOGGED_OR_NOT_OWNER": "You have no permission to modify this portfolio",
    "ERROR_ARTISTICNAME_BAD_PROVIDED": "The artistic name isn't valid",
    "ERROR_BIOGRAPHY_BAD_PROVIDED": "The biography isn't valid",
    "ERROR_BANNER_BAD_PROVIDED": "The banner isn't valid",
    "ERROR_BANNER_NOT_VALID_URL": "The banner URL isn't valid",
    "ERROR_BANNER_NOT_URL_IMAGE": "The banner URL does not correspond to an image",
    "ERROR_IMAGE_BAD_PROVIDED": "The image isn't valid",
    "ERROR_IMAGE_NOT_VALID_URL": "The image URL isn't valid",
    "ERROR_IMAGE_NOT_URL_IMAGE": "The image URL deson't correspond to an image",
    "ERROR_VIDEO_YOUTUBE": "The video isn't from YouTube",
    "ERROR_VIDEO_BAD_PROVIDED": "The video isn't valid",
    "ERROR_GENRE_NOT_FOUND": "The artistic genre doesn't exist",
    "ERROR_ZONE_NOT_FOUND": "The zone doesn't exist",
    "ERROR_MAINPHOTO_BAD_PROVIDED": "The main photo isn't valid",
    "ERROR_MAINPHOTO_NOT_VALID_URL": "The main photo URL isn't valid",
    "ERROR_MAINPHOTO_NOT_URL_IMAGE": "The main photo URL doesn't correspond to an image",
    "ERROR_PORTFOLIO_NOT_OWNER": "You can not edit this portfolio"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
