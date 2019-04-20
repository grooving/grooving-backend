spanish = {
    "ERROR_OFFER_NOT_FOUND": "Oferta no encontrada",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertence",
  "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
  "ERROR_NOT_A_CUSTOMER": "No eres un cliente, y por tanto no puedes estar en este sitio.",
  "ERROR_NO_CUSTOMER_FOUND": "El cliente que buscas no existe.",
  "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
  "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
  "ERROR_ACTOR_NOT_FOUND": "El actor que buscas no existe.",
  "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar."
}

english = {
    "ERROR_OFFER_NOT_FOUND": "Offer not found",
    "ERROR_NOT_OFFER_OWNER": "You are not the owner of the offer",
    "ERROR_NO_ARTISTIC_NAME": "You did not submit an artistic name.",
      "ERROR_NOT_LOGGED_IN": "You must be logged in to do this action.",
      "ERROR_NOT_A_CUSTOMER": "You are not a customer, and therefore you cannot be here.",
      "ERROR_NO_CUSTOMER_FOUND": "The customer you are searching for does not exist.",
      "ERROR_NO_DATA_GIVEN": "The form has no data.",
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
