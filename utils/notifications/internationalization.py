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
    "SUBJECT_DOWNLOAD_DATA_USER": "Solicitud de información personal",
    "BODY_DOWNLOAD_DATA_USER": "<p>Buenas, </p>" +
                               "<p>Cumpliendo con el <a href=\"https://gdpr-info.eu/art-20-gdpr/\">artículo 20</a> " +
                               "del GPDR (General Data Protection Regulation), le hemos enviado toda la información " +
                               "relativa sobre usted en un pdf adjunto a este correo.</p>" +
                               "<p>Un saludo.</p>"
}

english = {
    "WELCOME_SUBJECT": "Welcome to Grooving family",
    "BAN_UNBAN_USERS_ACTIVE_SUBJECT": "Your Grooving account has been actived again",
    "BAN_UNBAN_USERS_INACTIVE_SUBJECT": "Your Grooving account has been banned",
    "BREACH_NOTIFICATION_BODY": "<p>We inform you that we have detected a security breach in our system that we " +
                                "inform you about the Grooving accounts. We have taken steps to secure your account " +
                                "and are working closely with law enforcement authorities.</p>",
    "RIGHT_TO_BE_FORGOTTEN_BODY": "<p>Hello,</p>" +
                                  "<p>We appreciate you having contacting us.</p>" +
                                  "<p>We have carried out the procedure to apply your right to oblivion and has " +
                                  "performed correctly.</p>" +
                                  "<p>Best regards.</p>",
    "SUBJECT_DOWNLOAD_DATA_USER": "Personal information request",
    "BODY_DOWNLOAD_DATA_USER": "<p>Hello, </p>" +
                               "<p>In compliance with <a href=\"https://gdpr-info.eu/art-20-gdpr/\">artículo 20</a> " +
                               "of the GPDR (General Data Protection Regulation), we have sent you all the relative " +
                               "information about you in a pdf attached to this email.</p>" +
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
    "PDF_DOWNLOAD_DATA_ARTIST": "pdf_download_data_artist_es.html",
    "PDF_DOWNLOAD_DATA_CUSTOMER": "pdf_download_data_customer_es.html",
    "FOOTER": "footer_mail_es.html"
}

english_document = {
    "BODY_PENDING_TO_CONTRACT_MADE": "body_pending_to_contract_made_en.html",
    "PDF_PENDING_TO_CONTRACT_MADE": "pdf_pending_to_contract_made_en.html",
    "PDF_CONTRACT_MADE_TO_PAYMENT_MADE": "pdf_contract_made_to_payment_made_en.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_ARTIST": "pdf_contract_made_to_cancelled_artist_en.html",
    "PDF_CONTRACT_MADE_TO_CANCELLED_CUSTOMER": "pdf_contract_made_to_cancelled_customer_en.html",
    "PDF_DOWNLOAD_DATA_ARTIST": "pdf_download_data_artist_en.html",
    "PDF_DOWNLOAD_DATA_CUSTOMER": "pdf_download_data_customer_en.html",
    "FOOTER": "footer_mail_en.html"
}


def translate_render(key_language: str, document_to_translate: str, context: dict = None):
    translations_document = {
        "es": spanish_document,
        "en": english_document
    }

    return render_to_string(translations_document[key_language][document_to_translate], context)
