spanish = {
    "ERROR_DATE_FORMAT": "La fecha debe de seguir el siguiente formato: YYYY-MM-DDTHH:mm:ss",
    "ERROR_NULL_PAYMENT_CODE": "El código de pago no existe",
    "ERROR_OFFER_NOT_FOUND": "La oferta no existe",
    "ERROR_OFFER_NOT_OWNER": "No eres el propietario de la oferta",
    "ERROR_PAYMENT_COMPLETED": "El pago ya ha sido completado o la oferta ya ha finalizado",
    "ERROR_PAYPAL_NOT_RESPONSE": "No hay respuesta de PayPal",
    "ERROR_TOKEN_NOT_TAKEN": "No se ha pasado el token",
    "ERROR_PAYAPAL_CREDENTIALS": "Las credenciales de PayPal no son correctas",
    "ERROR_BRAINTREE_CREDENTIALS": "Las credenciales de Braintree no son correctas",
    "ERROR_PAYMENT_NOT_RESPONSE": "No hay respuesta del pago",
    "ERROR_OFFER_PAST_DATE": "La oferta es pasada",
    "ERROR_STATUS_NOT_PROVIDED": "El estado de la oferta no ha sido aportado",
    "ERROR_STATUS_NOT_CHANGED": "El estado de la oferta no ha sido modificado",
    "ERROR_BRAINTREE_ENV_NOT_SET": "El entorno de Braintree no ha sido configurado",
    "ERROR_TRANSACTION_STATUS_NOT_ALLOWED": "El estado de la transaccón no esta permitida",
    "ERROR_USER_NOT_AUTHORIZED": "Usuario no autorizado",
    "ERROR_DESCRIPTION_NOT_PROVIDED": "No se ha suministrado la descripción",
    "ERROR_DATE_NOT_PROVIDED": "No se ha suministrado la fecha",
    "ERROR_DATE_PAST": "La fecha no puede ser pasada",
    "ERROR_PAYMENTPACKAGE_NOT_PROVIDED": "No se ha suministrado un paquete de pago",
    "ERROR_PAYMENTPACKAGE_NOT_FOUND": "El paquete de pago no existe",
    "ERROR_HOURS_NOT_PROVIDED": "No se ha suministrado las horas",
    "ERROR_HOURS_BAD_PROVIDED": "El valor de horas no es válido",
    "ERROR_PRICE_NOT_PROVIDED": "No se ha suministrado el precio",
    "ERROR_PRICE_BELOW_MUNIMUM": "El valor del precio está por debajo del mínimo",
    "ERROR_EVENTLOCATION_NOT_PROVIDED": "No se ha suministrado la localización del evento",
    "ERROR_EVENTLOCATION_NOT_FOUND": "La localización del evento no existe",
    "ERROR_EVENTLOCATION_CAN_NOT_ASSIGNED": "No puedes asignar esta localización",
    "ERROR_CUSTOMER_NOT_FOUND": "El cliente no existe"
}

english = {
    "ERROR_DATE_FORMAT": "Date must follow this format: YYYY-MM-DDTHH:mm:ss",
    "ERROR_NULL_PAYMENT_CODE": "Payment code hasn't exist",
    "ERROR_OFFER_NOT_FOUND": "Offer don't exist",
    "ERROR_OFFER_NOT_OWNER": "You aren't owner of this offer",
    "ERROR_PAYMENT_COMPLETED": "Payment has been completed already or it's a past offer",
    "ERROR_PAYPAL_NOT_RESPONSE": "There isn't PayPal response",
    "ERROR_TOKEN_NOT_TAKEN": "Token hasn't been taken",
    "ERROR_PAYAPAL_CREDENTIALS": "Incorrect PayPal credentials",
    "ERROR_BRAINTREE_CREDENTIALS": "Incorrect Braintree credentials",
    "ERROR_PAYMENT_NOT_RESPONSE": "There isn't payment response",
    "ERROR_OFFER_PAST_DATE": "It's a past offer",
    "ERROR_STATUS_NOT_PROVIDED": "Offer status hasn't been provided",
    "ERROR_STATUS_NOT_CHANGED": "Offer status hasn't been changed",
    "ERROR_BRAINTREE_ENV_NOT_SET": "Braintree enviroment hasn't been set up",
    "ERROR_TRANSACTION_STATUS_NOT_ALLOWED": "Status transaction hasn't been allowed",
    "ERROR_USER_NOT_AUTHORIZED": "User isn't authorized",
    "ERROR_DESCRIPTION_NOT_PROVIDED": "Description hasn't provided",
    "ERROR_DATE_NOT_PROVIDED": "Date hasn't provided",
    "ERROR_DATE_PAST": "Date can't be pass",
    "ERROR_PAYMENTPACKAGE_NOT_PROVIDED": "Payment packege hasn't provided",
    "ERROR_PAYMENTPACKAGE_NOT_FOUND": "Payment packages doesn't exist",
    "ERROR_HOURS_NOT_PROVIDED": "Hours hasn't provided",
    "ERROR_HOURS_BAD_PROVIDED": "Hours value isn't valid",
    "ERROR_PRICE_NOT_PROVIDED": "Price hasn't provided",
    "ERROR_PRICE_BELOW_MUNIMUM": "Price value is below of minimum price",
    "ERROR_EVENTLOCATION_NOT_PROVIDED": "Event location hasn't provided",
    "ERROR_EVENTLOCATION_NOT_FOUND": "Event location hasn't exist",
    "ERROR_EVENTLOCATION_CAN_NOT_ASSIGNED": "Event location can't be assigned",
    "ERROR_CUSTOMER_NOT_FOUND": "Customer doesn't exist"
}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
