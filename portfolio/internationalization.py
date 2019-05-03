spanish = {
    "ERROR_PORTFOLIO_NOT_FOUND": "El portfolio no existe",
    "ERROR_NOT_LOGGED_OR_NOT_OWNER": "El usuario no esta logeado o el portfolio no le pertenece",
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

}

english = {
    "ERROR_BIOGRAPHY_TOO_LONG": "The biography is too long.",
    "ERROR_ARTISTICNAME_TOO_LONG": "The artistic name is too long.",
    "ERROR_URL_TOO_LONG": "The URL is too long. Limit is 500 characters.",
    "ERROR_STRING_TOO_LONG": "The string is too long",
    "ERROR_PORTFOLIO_NOT_FOUND": "Portfolio doesn't exist",
    "ERROR_NOT_LOGGED_OR_NOT_OWNER": "User not logged or isn't portfolio owner",
    "ERROR_ARTISTICNAME_BAD_PROVIDED": "Artistic name isn't valid",
    "ERROR_BIOGRAPHY_BAD_PROVIDED": "Biography isn't valid",
    "ERROR_BANNER_BAD_PROVIDED": "Banner isn't valid",
    "ERROR_BANNER_NOT_VALID_URL": "Banner URL isn't valid",
    "ERROR_BANNER_NOT_URL_IMAGE": "Banner URL isn't an image",
    "ERROR_IMAGE_BAD_PROVIDED": "Image isn't valid",
    "ERROR_IMAGE_NOT_VALID_URL": "Image URL isn't valid",
    "ERROR_IMAGE_NOT_URL_IMAGE": "Image URL isn't an image",
    "ERROR_VIDEO_YOUTUBE": "Video isn't from YouTube",
    "ERROR_VIDEO_BAD_PROVIDED": "Video isn't valid",
    "ERROR_GENRE_NOT_FOUND": "Artistic genre doesn't exist",
    "ERROR_ZONE_NOT_FOUND": "Zone doesn't exist",
    "ERROR_MAINPHOTO_BAD_PROVIDED": "Main photo isn't valid",
    "ERROR_MAINPHOTO_NOT_VALID_URL": "Main photo URL isn't valid",
    "ERROR_MAINPHOTO_NOT_URL_IMAGE": "Main photo URL isn't an image"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
