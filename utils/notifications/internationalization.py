from django.template.loader import render_to_string

spanish = {
    "WELCOME_SUBJECT": "Bienvenido a Grooving",
    "BAN_UNBAN_USERS_ACTIVE_SUBJECT": "¡Tu cuenta de Grooving ha sido activada de nuevo!",
    "BAN_UNBAN_USERS_INACTIVE_SUBJECT": "Tu cuenta de Grooving ha sido bloqueada",
    "BREACH_NOTIFICATION_BODY": "<p>Te informamos de que hemos detectado una brecha de seguridad en nuestro sistema " +
                                "que afecta a la información de varias cuentas de Grooving. Hemos tomado medidas " +
                                "para asegurar su cuenta y estamos trabajando estrechamente con las " +
                                "autoridades policiales.</p>",
    "RIGHT_TO_BE_FORGOTTEN_BODY": "<p>Buenas,</p>" +
                                  "<p>En primer lugar, le agradecemos que haya contado con nosotros.</p>" +
                                  "<p>Hemos llevado a cabo el procedimiento para aplicar su derecho al olvido y se "
                                  "ha realizado correctamente. </p>" +
                                  "<p>Un saludo.</p>",
}

english = {
    "WELCOME_SUBJECT": "Welcome to Grooving family",
    "BAN_UNBAN_USERS_ACTIVE_SUBJECT": "Your Grooving account has been actived again",
    "BAN_UNBAN_USERS_INACTIVE_SUBJECT": "Your Grooving account has been banned",
    "RIGHT_TO_BE_FORGOTTEN_BODY": "<p>Hello,</p>" +
                                  "<p>We appreciate you having contacting us.</p>" +
                                  "<p>We have carried out the procedure to apply your right to oblivion and has " +
                                  "performed correctly.</p>" +
                                  "<p>Best regards.</p>"
}


def translate(key_language: str, key_to_translate: str):

    translations = {
        "es": spanish,
        "en": english
    }

    return translations[key_language][key_to_translate]


spanish_document = {
    "BODY_PENDING_TO_CONTRACT_MADE": "body_pending_to_contract_made_es.html",
    "PDF_PENDING_TO_CONTRACT_MADE": "pdf_pending_to_contract_made_es.html",
    "PDF_CONTRACT_MADE_TO_PAYMENT_MADE": "pdf_contract_made_to_payment_made_es.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_ARTIST": "pdf_contract_made_to_cancelled_artist_es.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_CUSTOMER": "pdf_contract_made_to_cancelled_customer_es.html",
    "FOOTER": "footer_mail_es.html"
}

english_document = {
    "BODY_PENDING_TO_CONTRACT_MADE": "body_pending_to_contract_made_en.html",
    "PDF_PENDING_TO_CONTRACT_MADE": "pdf_pending_to_contract_made_en.html",
    "PDF_CONTRACT_MADE_TO_PAYMENT_MADE": "pdf_contract_made_to_payment_made_en.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_ARTIST": "pdf_contract_made_to_cancelled_artist_en.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_CUSTOMER": "pdf_contract_made_to_cancelled_customer_en.html",
    "FOOTER": "footer_mail_en.html"
}


def translate_render(key_language: str, document_to_translate: str, context: dict = None):
    translations_document = {
        "es": spanish_document,
        "en": english_document
    }

    return render_to_string(translations_document[key_language][document_to_translate], context)
