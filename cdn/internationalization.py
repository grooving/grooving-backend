spanish = {
    "ERROR_NOT_LOG_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_MUST_HAVE_DATA_AND_EXTENSION": "La imagen no es válida.",
    "ERROR_NOT_TYPE_NEW_IMAGE_ARTIST": "Donde desea mostrar la imagen no existe.",
    "ERROR_NOT_TYPE_NEW_IMAGE_CUSTOMER": "Donde desea mostrar la imagen no existe.",
    "ERROR_CAROUSEL_PHOTO_LIMIT_IS_TEN": "Solo puede tener 10 imágenes en el portafolio.",
    "ERROR_IMAGE_MORE_THAN_2MB": "La imagen debe tener un tamaño máximo de 1,5 MB.",

}

english = {
    "ERROR_NOT_LOG_IN": "You must be logged in to access this page.",
    "ERROR_MUST_HAVE_DATA_AND_EXTENSION": "Image is not valid.",
    "ERROR_NOT_TYPE_NEW_IMAGE_ARTIST": "Where you want to show the image does not exist.",
    "ERROR_NOT_TYPE_NEW_IMAGE_CUSTOMER": "Where you want to show the image does not exist.",
    "ERROR_CAROUSEL_PHOTO_LIMIT_IS_TEN": "You can only have 10 images in your portfolio.",
    "ERROR_IMAGE_MORE_THAN_2MB": "The image must have a maximum size of 1.5 MB.",

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}

