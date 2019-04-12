from django.core.mail import EmailMessage
from Grooving.models import Offer, SystemConfiguration, User
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import datetime


class Notifications:

    @staticmethod
    def footer():
        return render_to_string('footer_mail.html')

    @staticmethod
    def send_email_welcome(user_id):

        user = User.objects.get(pk=user_id)

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'
        email.content_subtype = 'html'

        email.to = [user.email]
        email.subject = "Welcome to Grooving family"
        email.body = "<p>Hi there,</p>" \
                     "<p>Congratulations! You've signing with Grooving and are now part of a community that connects " \
                     "artists and improve their visibility in an easy, simple, simple and reliable way. " \
                     "From now, you'll get regular updates on the offers status made and all the information related" \
                     " to them. </p>" \
                     "<p>Your username is: <b>" + user.username + "</b></p>" \
                                                                  "<p>Cheers,</p>" \
                                                                  "<p>Grooving team</p>" \
                     + Notifications.footer()
        email.send()

    @staticmethod
    def send_email_create_an_offer(offer_id):
        offer = Offer.objects.get(pk=offer_id)

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'
        email.content_subtype = 'html'

        # email.to = ['utri1990@gmail.com']
        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        email.subject = "You received a new offer to " + offer.paymentPackage.portfolio.artisticName
        email.body = '<h1>' + offer.eventLocation.customer.user.get_full_name() + \
                     ' has contacted you. </h1><p>Come on! See the details on the webpage.<p>' + Notifications.footer()
        email.send()

        email.to = [offer.eventLocation.customer.user.email]
        # email.to = ['utri1990@gmail.com']
        email.subject = 'You has sent a offer!'
        email.body = '<h1>Your offer has been send to ' + offer.paymentPackage.portfolio.artisticName + '</h1>' + \
                     '<p>You will receive more information soon. </p>' + Notifications.footer()
        email.send()

    @staticmethod
    def send_email_pending_to_rejected(offer_id):
        offer = Offer.objects.get(pk=offer_id)

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'

        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        # email.to = ['utri1990@gmail.com']
        email.subject = 'The offer has been rejected successfully'
        email.content_subtype = 'html'
        email.body = 'You have rejected the offer received from ' + offer.eventLocation.customer.user.get_full_name() \
                     + Notifications.footer()
        email.send()

        email.to = [offer.eventLocation.customer.user.email]
        # email.to = ['utri1990@gmail.com']
        email.subject = 'Your offer has been rejected'
        email.content_subtype = 'html'
        email.body = 'We are sorry. The offer sent to ' + offer.paymentPackage.portfolio.artisticName + \
                     ' has been rejected.' + Notifications.footer()
        email.send()

    @staticmethod
    def send_email_pending_to_withdrawn(offer_id):
        offer = Offer.objects.get(pk=offer_id)

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'

        # email.to = ['utri1990@gmail.com']
        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        email.subject = 'The offer has been withdrawn'
        email.body = 'We are sorry. ' + offer.eventLocation.customer.user.get_full_name() + ' ' \
                     'has withdrawn the offer.' + Notifications.footer()
        email.content_subtype = 'html'
        email.send()

        email.to = [offer.eventLocation.customer.user.email]
        # email.to = ['utri1990@gmail.com']
        email.subject = 'The offer has been withdrawn successfully.'
        email.body = 'You have withdrawn the offer sent to ' + offer.paymentPackage.portfolio.artisticName + "." \
                     + Notifications.footer()
        email.content_subtype = 'html'
        email.send()

    @staticmethod
    def send_email_pending_to_contract_made(offer_id):
        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Template

        # Template - Data to generate email body & pdf

        context_body = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_description': offer.eventLocation.description,
            'event_date': offer.date.strftime('%Y-%m-%d'),
            'event_duration': offer.hours,
            'event_hour': offer.date.strftime('%H:%M'),
            'event_price': offer.price,
            'event_currency': offer.currency,
            'event_equipment': offer.eventLocation.equipment,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
        }

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_description': offer.eventLocation.description,
            'event_date': offer.date.strftime('%Y-%m-%d'),
            'event_duration': offer.hours,
            'event_hour': offer.date.strftime('%H:%M'),
            'event_price': offer.price,
            'event_currency': offer.currency,
            'event_equipment': offer.eventLocation.equipment,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit,
        }

        # Check package type (necessary for generate pdf & email information)

        if offer.paymentPackage.performance is not None:
            context_pdf['event_payment_package'] = 'Performance'  # Informaremos el precio total y la duración
            context_body['event_payment_package'] = 'Performance'
        elif offer.paymentPackage.fare is not None:
            context_pdf['event_payment_package'] = 'Fare'  # Informaremos del precio multiplicado por la hora
            context_pdf['event_payment_package_price_per_hour'] = offer.paymentPackage.fare.priceHour
            context_body['event_payment_package'] = 'Fare'
        else:
            context_pdf['event_payment_package'] = 'Custom'  # Informaremos del precio total y la duración
            context_body['event_payment_package'] = 'Custom'

        pdf_html = render_to_string("pdf_pending_to_contract_made.html", context_pdf)

        # Email

        email = EmailMessage()
        email.subject = 'Offer accepted'
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'
        email.content_subtype = 'html'
        pdf_file = HTML(string=pdf_html).write_pdf()
        email.attach('contract.pdf', pdf_file, 'application/pdf')

        # Artist mail

        context_body['title'] = 'Congratulations! You have been hired by ' + \
                                offer.eventLocation.customer.user.get_full_name()
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        email.body = render_to_string("body_pending_to_contract_made.html", context_body) + Notifications.footer()
        email.send()  # Sending email

        # Customer mail

        context_body['title'] = 'Done! You have hired ' + offer.paymentPackage.portfolio.artisticName
        context_body['event_payment_code'] = offer.paymentCode
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.eventLocation.customer.user.email]
        email.body = render_to_string("body_pending_to_contract_made.html", context_body) + Notifications.footer()

        email.send()  # Sending email

    @staticmethod
    def send_email_contract_made_to_payment_made(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Template - Artist pdf

        artist_benefit = round(offer.price - offer.price * (system_configuration.profit / 100), 2)

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_corporate_email': system_configuration.corporateEmail,
            'event_date_now': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'event_duration': offer.hours,
            'event_total': offer.price,
            'event_currency': offer.currency,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit.normalize(),
            'invoice_grooving_benefit': round(offer.price * (system_configuration.profit / 100), 2),
            'invoice_artist_benefit': artist_benefit,
        }

        pdf_html = render_to_string("pdf_contract_made_to_payment_made.html", context_pdf)

        # Email

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'
        email.content_subtype = 'html'

        # Customer mail

        email.subject = offer.paymentPackage.portfolio.artisticName + ' performance is over'
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.eventLocation.customer.user.email]
        email.body = '<p>We hope you enjoyed to ' + offer.paymentPackage.portfolio.artisticName + ' performance.<p>'\
                     + Notifications.footer()

        email.send()  # Sending email

        # Artist mail

        email.subject = 'The payment has been realized'
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        email.body = '<h1>You have received the payment in your account </h1>' \
                     '<p>You can see the details on pdf attachment.<p>' + Notifications.footer()
        email.attach('contract.pdf', pdf_file, 'application/pdf')
        email.send()  # Sending email

    @staticmethod
    def send_email_contract_made_to_cancelled_artist(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Template - Artist pdf

        artist_benefit = round(offer.price - offer.price * (system_configuration.profit / 100), 2)

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_corporate_email': system_configuration.corporateEmail,
            'event_date_now': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'event_duration': offer.hours,
            'event_total': offer.price,
            'event_currency': offer.currency,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit.normalize(),
            'invoice_grooving_benefit': round(offer.price * (system_configuration.profit / 100), 2),
            'invoice_customer_benefit': artist_benefit,
        }

        pdf_html = render_to_string("pdf_contract_made_to_cancelled_artist.html", context_pdf)

        # Email

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'
        email.content_subtype = 'html'

        # Artist mail

        email.subject = 'The performance has been cancelled by you'
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        email.body = '<p>We are sorry that that this decision.</>' \
                     '<p>See you soon!<p>' + Notifications.footer()
        email.send()  # Sending email

        # Customer mail

        email.subject = offer.paymentPackage.portfolio.artisticName + 'has cancelled the performance'
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.eventLocation.customer.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        email.body = '<p>We are sorry that the performance has been cancelled. We proceed to return the money to your' \
                     ' account.</p>' + Notifications.footer()
        email.attach('invoice.pdf', pdf_file, 'application/pdf')
        email.send()  # Sending email

    @staticmethod
    def send_email_contract_made_to_cancelled_customer(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Template - Artist pdf

        artist_benefit = round(offer.price - offer.price * (system_configuration.profit / 100), 2)

        context_pdf = {
            'customer_name': offer.eventLocation.customer.user.get_full_name(),
            'artist_artisticName': offer.paymentPackage.portfolio.artisticName,
            'artist_name': offer.paymentPackage.portfolio.artist.user.get_full_name(),
            'event_name': offer.eventLocation.name,
            'event_address': offer.eventLocation.address,
            'event_corporate_email': system_configuration.corporateEmail,
            'event_date_now': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'event_duration': offer.hours,
            'event_total': offer.price,
            'event_currency': offer.currency,
            'system_configuration_terms_and_conditions': system_configuration.termsText,
            'system_configuration_profit': system_configuration.profit.normalize(),
            'invoice_grooving_benefit': round(offer.price * (system_configuration.profit / 100), 2),
            'invoice_customer_benefit': artist_benefit,
        }

        pdf_html = render_to_string('pdf_contract_made_to_cancelled_customer.html', context_pdf)

        # Email

        email = EmailMessage()
        email.from_email = 'Grooving <no-reply@grupogrooving.com>'
        email.content_subtype = 'html'

        # Artist mail

        email.subject = 'The performance has been cancelled by ' + offer.eventLocation.customer.user.get_full_name()
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.paymentPackage.portfolio.artist.user.email]
        email.body = '<p>We are sorry that the performance has been cancelled.</p>' \
                     '<p>See you soon!</p>' + Notifications.footer()
        email.send()  # Sending email

        # Customer mail

        email.subject = 'You cancelled the performance'
        # email.to = ['utri1990@gmail.com']
        email.to = [offer.eventLocation.customer.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        email.body = '<p>We are sorry that this decision. We proceed to return the money to your account.</p>' + \
                     Notifications.footer()
        email.attach('invoice.pdf', pdf_file, 'application/pdf')
        email.send()  # Sending email
