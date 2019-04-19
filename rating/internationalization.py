spanish = {
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence",
    "ERROR_NO_SCORE": "Debes dar una puntuacion al artista.",
  "ERROR_DECIMAL_SCORE": "La puntuacion debe ser un numero sin decimales.",
  "ERROR_RATING_OUT_OF_RANGE": "La puntuacion debe estar entre 1 y 5.",
  "ERROR_OFFER_NOT_OWNED": "Esta oferta no te pertenece.",
  "ERROR_OFFER_NOT_READY": "Esta oferta no puede recibir una puntuacion, pues aun no se ha hecho el pago.",
  "ERROR_OFFER_ALREADY_RATED": "Esta oferta ya tiene una puntuacion. No puedes puntuarla dos veces.",
  "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_USER": "El usuario relacionado con esta oferta ha borrado sus datos, por lo que esta oferta no puede ser puntuada."

}

english = {
    "ERROR_NO_SCORE": "You must give a score.",
    "ERROR_DECIMAL_SCORE": "The rating must be a number with no decimals.",
    "ERROR_RATING_OUT_OF_RANGE": "The rating must be between 1 and 5 points.",
    "ERROR_OFFER_NOT_OWNED": "This offer is not yours.",
    "ERROR_OFFER_NOT_READY": "This offer cannot receive a rating yet, since it has not been paid yet.",
    "ERROR_OFFER_ALREADY_RATED": "This offer is already rated. You cannot rate it twice.",
    "ERROR_OFFER_NOT_FOUND": "The offer you are searching for does not exist.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_USER": "The user related to this offer has deleted their data, so this offer cannot be rated."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
