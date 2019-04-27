spanish = {
    "ERROR_NO_USER": "No hay usuarios de este tipo",
    "ERROR_NOT_LOGGED_IN": "Debes estar autenticado para entrar en este sitio.",
    "ERROR_FARE_PACKAGE_ALREADY_CREATED": "Ya has creado un paquete de tarifa.",
    "ERROR_CUSTOM_PACKAGE_ALREADY_CREATED": "Ya has creado un paquete personalizado.",
    "ERROR_PRICE_NOT_PROVIDED": "Precio no indicado.",
    "ERROR_INVALID_PRICE": "Precio inválido.",
    "ERROR_PAYMENT_PACKAGE_NOT_FOUND": "Paquete de pago no encontrado",
    "ERROR_FARE_PACKAGE_NOT_FOUND": "Paquete de tarifa no encontrado",
    "ERROR_CUSTOM_PACKAGE_NOT_FOUND": "Paquete personalizado no encontrado",
    "ERROR_PERFORMANCE_PACKAGE_NOT_FOUND": "Paquete de actuaciones no encontrado",
    "ERROR_MINIMUM_PRICE_NOT_PROVIDED": "Precio mínimo no indicado",
    "ERROR_HOURS_NOT_PROVIDED": "Número de horas no indicada",
    "ERROR_INVALID_HOURS": "El número de horas indicado es inválido.",
    "ERROR_INFO_NOT_PROVIDED": "Información no indicada.",
    "ERROR_MUST_BE_LOGGED": "No estás logueado.",
    "ERROR_NOT_OWNER": "No eres el dueño de este paquete de pago.",
    "ERROR_CUSTOM_PACKAGE_NOT_OWNER": "No eres el dueño de este paquete de pago personalizado.",
    "ERROR_PERFORMANCE_PACKAGE_NOT_OWNER": "No eres el dueño de este paquete de actuación.",
    "ERROR_FARE_PACKAGE_NOT_OWNER": "No eres el dueño de esta tarifa.",

}

english = {
    "ERROR_NO_USER": "There are no users of this type",
    "ERROR_NOT_LOGGED_IN": "You must be logged in to access this page.",
    "ERROR_FARE_PACKAGE_ALREADY_CREATED": "You already have a fare package.",
    "ERROR_CUSTOM_PACKAGE_ALREADY_CREATED": "You already have a custom package.",
    "ERROR_PRICE_NOT_PROVIDED": "Price not provided",
    "ERROR_INVALID_PRICE": "Invalid price.",
    "ERROR_PAYMENT_PACKAGE_NOT_FOUND": "Payment package not found",
    "ERROR_FARE_PACKAGE_NOT_FOUND": "Fare package not found.",
    "ERROR_CUSTOM_PACKAGE_NOT_FOUND": "Custom package not found",
    "ERROR_PERFORMANCE_PACKAGE_NOT_FOUND": "Performance package not found",
    "ERROR_MINIMUM_PRICE_NOT_PROVIDED": "Minimum price not provided.",
    "ERROR_HOURS_NOT_PROVIDED": "Hours not provided",
    "ERROR_INFO_NOT_PROVIDED": "Info not provided.",
    "ERROR_INVALID_HOURS": "Invalid hours number.",
    "ERROR_MUST_BE_LOGGED": "You are not logged in.",
    "ERROR_NOT_OWNER": "You are not the owner of this payment package.",
    "ERROR_CUSTOM_PACKAGE_NOT_OWNER": "You are not the owner of this custom package.",
    "ERROR_PERFORMANCE_PACKAGE_NOT_OWNER": "You are not the owner of this performance package.",
    "ERROR_FARE_PACKAGE_NOT_OWNER": "You are not the owner of this fare package.",


}


def translate(keyLanguage: str, keyToTranslate: str):
    translations = {
        "es": spanish,
        "en": english
    }

    return {"error": translations[keyLanguage][keyToTranslate]}
