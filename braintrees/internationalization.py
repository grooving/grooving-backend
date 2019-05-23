spanish = {

    "ERROR_INCORRECT_ID": "No se ha proporcionado una ID.",
    "ERROR_IN_CREATION": "Error durante la creacion, intentelo de nuevo",
    "ERROR_NO_CUSTOMER": "Este usuario no es un cliente",
    "ERROR_CUSTOMER": "Error creando el cliente braintree",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_NO_DATA_GIVEN": "El formulario no tiene datos.",
    "ERROR_NO_MATCHING_LANGUAGE": "El idioma que has escogido no esta disponible.",
    "ERROR_NO_GIVEN_LANGUAGE": "Debes indicar un idioma al que cambiar.",
    "ERROR_NO_OFFER": "No existe esta oferta.",
    "ERROR_OFFER_CUSTOMER": "Esta oferta no pertenece a este cliente.",
    "ERROR_AMOUNT" : "La cantidad no puede ser menor o igual que 0",
    "ERROR_PAYMENT" : "Pago no procesado. Compruebe los datos introducidos",
    "ERROR_RESPONSE" : "No hay respuesta desde Paypal",
    "ERROR_CREDENTIAL" : "Error de credenciales de Paypal",
    "ERROR_ENVIROMENT" : "Entorno de Braintree no configurado",
    "ERROR_TOKEN" : "Error en la generacion del token"
}

english = {

    "ERROR_INCORRECT_ID": "No id given.",
    "ERROR_IN_CREATION": "Error during the creation, try again",
    "ERROR_NO_CUSTOMER": "This user is not a customer",
    "ERROR_CUSTOMER": "Error creating braintree customer",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_NO_DATA_GIVEN": "The form has no data.",
    "ERROR_NO_MATCHING_LANGUAGE": "This language is not available.",
    "ERROR_NO_GIVEN_LANGUAGE": "You must choose a language.",
    "ERROR_NO_OFFER": "The offer does not exist.",
    "ERROR_OFFER_CUSTOMER": "The offer does not belong to this customer.",
    "ERROR_AMOUNT" : "Amount is 0 or lower",
    "ERROR_PAYMENT" : "Your payment could not be processed. Please check your input or use another payment method and try again",
    "ERROR_RESPONSE" : "No response from Paypal",
    "ERROR_CREDENTIAL" : "Credential error with paypal",
    "ERROR_ENVIROMENT" : "Enviroment in Braintree not set",
    "ERROR_TOKEN" : "There was an error generating the token"

}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
