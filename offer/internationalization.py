spanish = {
    "ERROR_PAYMENT_CODE_NOT_PROVIDED": "Código de pago no encontrado.",
    "ERROR_PAYMENT_MADE_OR_OUTDATED": "El pago ha sido realizado o está desactualizado.",
    "ERROR_PAYPAL_NOT_RESPONSE": "No hay respuesta desde Paypal",
    "ERROR_PAYPAL_CANT_TAKE_TOKEN": "Paypal no coge el token.",
    "ERROR_PAYPAL_NEED_ACCOUNT": "Necesitas una cuenta de paypal para realizar esta acción.",
    "ERROR_PAYPAL_NO_RESPONSE_TO_PAY": "No recibo respuesta a la hora de realizar el pago.",
    "ERROR_OFFER_NOT_EXISTS": "La oferta no existe.",
    "ERROR_OFFER_NOT_FOUND": "La oferta no se ha añadido.",
    "ERROR_OFFER_IN_THE_PAST": "La oferta ocurrió en el pasado.",
    "ERROR_STATUS_NOT_FOUND": "El estado no ha sido especificado.",
    "ERROR_STATUS_ISNT_CHANGED": "El estado no ha sido cambiado",
    "ERROR_BRAINTREE_ENVIRONMENT_NOT_SET": "Entorno de braintree no especificado.",
    "ERROR_BRAINTREE_OFFER_HAVENT_CREDENTIALS": "La oferta no posee los credenciales de Braintree.",
    "ERROR_EMPTY_DESCRIPTION": "La descripción no debe estar vacía.",
    "ERROR_EMPTY_DATE": "La fecha no debe estar vacía",
    "ERROR_DATE_FORMAT": "El formato no es el correcto. Debería ser YYYY-MM-DDTHH:mm:ss",
    "ERROR_DATE_IS_PAST": "La fecha es pasada.",
    "ERROR_EMPTY_PAYMENT_PACKAGE_ID": "El id del paquete de pago no debe estar vacío.",
    "ERROR_EMPTY_PAYMENT_PACKAGE": "El paquete de pago no existe.",
    "ERROR_EMPTY_HOURS": "El campo hora no debe estar vacío.",
    "ERROR_BAD_HOURS": "El campo hora es erróneo.",
    "ERROR_EMPTY_PRICE": "El campo precio no debe estar vacío.",
    "ERROR_PRICE_MINIMUM_EXCEPTION": "El precio indicado está por debajo de lo permitido.",
    "ERROR_EMPTY_EVENT_LOCATION": "El campo localización del evento no debe estar vacío.",
    "ERROR_EVENT_LOCATION_DOESNT_EXISTS": "El campo localización del evento no existe.",
    "ERROR_EVENT_LOCATION_CANT_REFERENCE": "El campo localización del evento no puede referenciarse al customer.",
    "ERROR_NOT_ALLOWED_TRANSITION": "Transición no permitida.",

    "ERROR_ARTIST_NOT_LOGGED": "Permiso denegado.",
    "ERROR_CUSTOMER_NOT_LOGGED": "Permiso denegado.",
    "ERROR_EMPTY_FORM": "El formulario no puede estar vacío.",
    "ERROR_OFFER_NOT_FOR_YOURSELF": "La oferta no es para tí.",
    "ERROR_NOT_OFFER_OWNER": "La oferta no te pertenece.",
    "ERROR_USER_NOT_AUTHORIZED": "El usuario no ha sido autorizado.",
    "ERROR_CUSTOMER_NOT_FOUND": "El cliente no funciona."

}

english = {
    "ERROR_PAYMENT_CODE_NOT_PROVIDED": "Payment code not provided.",
    "ERROR_PAYMENT_MADE_OR_OUTDATED": "The payment has already been made or is outdated",
    "ERROR_PAYPAL_NOT_RESPONSE": "Paypal does not answer.",
    "ERROR_PAYPAL_CANT_TAKE_TOKEN": "Paypal cannot take token.",
    "ERROR_PAYPAL_NEED_ACCOUNT": "You need to provide a PayPal account to perform this action.",
    "ERROR_PAYPAL_NO_RESPONSE_TO_PAY": "I can\'t receive a payment response.",
    "ERROR_OFFER_NOT_EXISTS": "Offer doesn\'t exists.",
    "ERROR_OFFER_NOT_FOUND": "Offer not found.",
    "ERROR_OFFER_IN_THE_PAST": "The offer occurred in the past",
    "ERROR_STATUS_NOT_FOUND": "Status field not provided.",
    "ERROR_STATUS_ISNT_CHANGED": "Status field provided isn\'t changed",
    "ERROR_BRAINTREE_ENVIRONMENT_NOT_SET": "Environment in Braintree not set",
    "ERROR_BRAINTREE_OFFER_HAVENT_CREDENTIALS": "Offer does not have Braintree credentials.",
    "ERROR_EMPTY_DESCRIPTION": "Description field not provided",
    "ERROR_EMPTY_DATE": "Date field not provided.",
    "ERROR_DATE_FORMAT": "The format is not correct. It should be YYYY-MM-DDTHH:mm:ss",
    "ERROR_DATE_IS_PAST": "Date value is past.",
    "ERROR_EMPTY_PAYMENT_PACKAGE_ID": "Payment package id field not provided",
    "ERROR_EMPTY_PAYMENT_PACKAGE": "Payment package doesn't exists.",
    "ERROR_EMPTY_HOURS": "Hours field not provided.",
    "ERROR_BAD_HOURS": "Hours value bad provided.",
    "ERROR_EMPTY_PRICE": "Price field not provided.",
    "ERROR_PRICE_MINIMUM_EXCEPTION": "Price entered it\'s below of minimum price",
    "ERROR_EMPTY_EVENT_LOCATION": "Event location field not provided.",
    "ERROR_EVENT_LOCATION_DOESNT_EXISTS": "Event location does not exist.",
    "ERROR_EVENT_LOCATION_CANT_REFERENCE": "Can\'t reference this eventLocation",
    "ERROR_NOT_ALLOWED_TRANSITION": "Transition isn\'t allowed.",

    "ERROR_ARTIST_NOT_LOGGED": "Permission denied.",
    "ERROR_CUSTOMER_NOT_LOGGED": "Permission denied.",
    "ERROR_EMPTY_FORM": "Empty form is not valid.",
    "ERROR_OFFER_NOT_FOR_YOURSELF": "The offer is not for yourself.",
    "ERROR_NOT_OFFER_OWNER": "You are not the owner of the offer.",
    "ERROR_USER_NOT_AUTHORIZED": "User not authorized.",
    "ERROR_CUSTOMER_NOT_FOUND": "Customer not found."
}


def translate(key_language: str, key_to_translate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[key_language][key_to_translate]}
