spanish = {
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence",
    "ERROR_NO_SCORE": "Debes dar una puntuacion al artista.",
  "ERROR_DECIMAL_SCORE": "La puntuacion debe ser un numero sin decimales.",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
  "ERROR_RATING_OUT_OF_RANGE": "La puntuacion debe estar entre 1 y 5.",
  "ERROR_OFFER_NOT_OWNED": "Esta oferta no te pertenece.",
  "ERROR_OFFER_NOT_READY": "Esta oferta no puede recibir una puntuacion, pues aun no se ha hecho el pago.",
  "ERROR_OFFER_ALREADY_RATED": "Esta oferta ya tiene una puntuacion. No puedes puntuarla dos veces.",
  "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_USER": "El usuario relacionado con esta oferta ha borrado sus datos, por lo que esta oferta no puede ser puntuada.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_ACTOR_NOT_FOUND": "El actor que buscas no existe.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_NOT_A_CUSTOMER": "No eres un cliente, y por tanto no puedes estar en este sitio.",
    "ERROR_NO_CUSTOMER_FOUND": "El cliente que buscas no existe.",

}

english = {
    "ERROR_NO_SCORE": "You must give a score.",
    "ERROR_NOT_A_CUSTOMER": "You are not a customer, and therefore you cannot be here.",
    "ERROR_NO_CUSTOMER_FOUND": "The customer you are searching for does not exist.",
    "ERROR_DECIMAL_SCORE": "The rating must be a number with no decimals.",
    "ERROR_RATING_OUT_OF_RANGE": "The rating must be between 1 and 5 points.",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to do this action.",
    "ERROR_OFFER_NOT_OWNED": "This offer is not yours.",
    "ERROR_OFFER_NOT_READY": "This offer cannot receive a rating yet, since it has not been paid yet.",
    "ERROR_OFFER_ALREADY_RATED": "This offer is already rated. You cannot rate it twice.",
    "ERROR_OFFER_NOT_FOUND": "The offer you are searching for does not exist.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_USER": "The user related to this offer has deleted their data, so this offer cannot be rated.",
    "ERROR_NO_MATCHING_LANGUAGE": "The language you want is not available.",
    "ERROR_ACTOR_NOT_FOUND": "The actor you are searching does not exist.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must give a language to switch to."
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
