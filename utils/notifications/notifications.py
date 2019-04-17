from django.core.mail import EmailMessage
from Grooving.models import Offer, SystemConfiguration, User
from weasyprint import HTML
from django.template.loader import render_to_string
from datetime import datetime
import threading


class EmailMessageThread(threading.Thread):

    def __init__(self, from_email, to, body, subject, body_content_type, list_attachments, fail_silently=False):
        self.from_email = from_email
        self.to = to
        self.body = body
        self.subject = subject
        self.body_content_type = body_content_type
        self.fail_silently = fail_silently
        self.list_attachments = list_attachments

        threading.Thread.__init__(self)

    def run(self):
        message = EmailMessage(from_email=self.from_email, to=self.to, body=self.body, subject=self.subject)
        message.content_subtype = self.body_content_type

        message.attachments = self.list_attachments

        '''
        How it works attachments on EmailMessage?

        - Traditional method:

        if self.list_attachments:
            for attachment in self.list_attachments:
                message.attach(attachment[0], attachment[1], attachment[2])  # filename, content, mimetype

        - Resume method:

        [message.attach(attachment[0], attachment[1], attachment[2]) for attachment in self.list_attachments
        if self.list_attachments]

        - Fast method:

        message.attachments = self.list_attachment
        '''

        message.send(fail_silently=self.fail_silently)

    @staticmethod
    def send_mail(from_email, to, body, subject, body_content_type, fail_silently):
        EmailMessageThread(from_email, to, body, subject, body_content_type, None, fail_silently).start()

    @staticmethod
    def send_mail_with_attachments(from_email, to, body, subject, body_content_type, list_attachments, fail_silently):
        EmailMessageThread(from_email, to, body, subject, body_content_type, list_attachments, fail_silently).start()


class Notifications:

    @staticmethod
    def footer():
        return render_to_string('footer_mail.html')

    @staticmethod
    def send_email_welcome(user_id):

        # Entity database objects

        user = User.objects.get(pk=user_id)

        # Email content

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'
        to = [user.email]
        subject = 'Welcome to Grooving family'
        body = "<p>Hi there,</p>" \
               "<p>Congratulations! You've signing with Grooving and are now part of a community that connects " \
               "artists and improve their visibility in an easy, simple, simple and reliable way. " \
               "From now, you'll get regular updates on the offers status made and all the information related" \
               " to them. </p>" \
               "<p>Your username is: <b>" + user.username + "</b></p>" \
                                                            "<p>Cheers,</p>" \
                                                            "<p>Grooving team</p>" \
               + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_create_an_offer(offer_id):

        # Entity database objects

        offer = Offer.objects.get(pk=offer_id)

        # Common email content

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist email

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = "You received a new offer to " + offer.paymentPackage.portfolio.artisticName
        body = '<h1>' + offer.eventLocation.customer.user.get_full_name() + \
               ' has contacted you. </h1><p>Come on! See the details on the webpage.<p>' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer email

        to = [offer.eventLocation.customer.user.email]
        subject = 'You has sent a offer!'
        body = '<h1>Your offer has been send to ' + offer.paymentPackage.portfolio.artisticName + '</h1>' + \
               '<p>You will receive more information soon. </p>' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_pending_to_rejected(offer_id):

        # Entity database objects

        offer = Offer.objects.get(pk=offer_id)

        # Common email content

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist email

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = 'The offer has been rejected successfully'
        body = 'You have rejected the offer received from ' + offer.eventLocation.customer.user.get_full_name() \
               + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer email

        to = [offer.eventLocation.customer.user.email]
        subject = 'Your offer has been rejected'
        body = 'We are sorry. The offer sent to ' + offer.paymentPackage.portfolio.artisticName + \
               ' has been rejected.' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_pending_to_withdrawn(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist email

        to = [offer.paymentPackage.portfolio.artist.user.email]
        subject = 'The offer has been withdrawn'
        body = 'We are sorry. ' + offer.eventLocation.customer.user.get_full_name() + \
               'has withdrawn the offer.' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer email

        to = [offer.eventLocation.customer.user.email]
        subject = 'The offer has been withdrawn successfully.'
        body = 'You have withdrawn the offer sent to ' + offer.paymentPackage.portfolio.artisticName + "." + \
               Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_pending_to_contract_made(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate email body & pdf

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

        # Check package type (necessary for generate pdf & body information)

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

        # Email - PDF generator

        pdf_html = render_to_string("pdf_pending_to_contract_made.html", context_pdf)

        # Email - Body generator for artist

        context_body['title'] = 'Congratulations! You have been hired by ' + \
                                offer.eventLocation.customer.user.get_full_name()

        body_artist_html = render_to_string("body_pending_to_contract_made.html", context_body) + Notifications.footer()

        # Email - Body generator for customer

        context_body['title'] = 'Done! You have hired ' + offer.paymentPackage.portfolio.artisticName
        context_body['event_payment_code'] = offer.paymentCode

        body_customer_html = render_to_string("body_pending_to_contract_made.html",
                                              context_body) + Notifications.footer()

        # Common email content

        subject = 'Offer accepted'
        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        pdf_file = HTML(string=pdf_html).write_pdf()  # Generating PDF

        # Artist mail

        to = [offer.paymentPackage.portfolio.artist.user.email]
        list_attachments = [('contract.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body_artist_html, subject, body_content_type,
                                                      list_attachments, True)

        # Customer mail

        to = [offer.eventLocation.customer.user.email]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body_customer_html, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod
    def send_email_contract_made_to_payment_made(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate email body & pdf

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

        # Common email content

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Customer mail

        subject = offer.paymentPackage.portfolio.artisticName + ' performance is over'
        to = [offer.eventLocation.customer.user.email]
        body = '<p>We hope you enjoyed to ' + offer.paymentPackage.portfolio.artisticName + ' performance.<p>' \
               + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Artist mail

        subject = 'The payment has been realized'
        to = [offer.paymentPackage.portfolio.artist.user.email]
        body = '<h1>You have received the payment in your account </h1>' \
               '<p>You can see the details on pdf attachment.<p>' + Notifications.footer()

        # Email - PDF generator to artist

        pdf_html = render_to_string("pdf_contract_made_to_payment_made.html", context_pdf)
        pdf_file = HTML(string=pdf_html).write_pdf()

        list_attachments = [('contract.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod
    def send_email_contract_made_to_cancelled_artist(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate pdf

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

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist mail

        subject = 'The performance has been cancelled by you'
        to = [offer.paymentPackage.portfolio.artist.user.email]
        body = '<p>We are sorry that this decision.</p><p>See you soon!<p>' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer mail

        subject = offer.paymentPackage.portfolio.artisticName + 'has cancelled the performance'
        to = [offer.eventLocation.customer.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        body = '<p>We are sorry that the performance has been cancelled. We proceed to return the money to your' \
               ' account.</p>' + Notifications.footer()

        list_attachments = [('invoice.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod
    def send_email_contract_made_to_cancelled_customer(offer_id):

        # Entity database objects (necessary from template & email)

        offer = Offer.objects.get(pk=offer_id)
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Data to generate pdf

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

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        body_content_type = 'html'

        # Artist mail

        subject = 'The performance has been cancelled by ' + offer.eventLocation.customer.user.get_full_name()
        to = [offer.paymentPackage.portfolio.artist.user.email]
        body = '<p>We are sorry that the performance has been cancelled.</p>' \
               '<p>See you soon!</p>' + Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

        # Customer mail

        subject = 'You cancelled the performance'
        to = [offer.eventLocation.customer.user.email]
        pdf_file = HTML(string=pdf_html).write_pdf()
        body = '<p>We are sorry that this decision. We proceed to return the money to your account.</p>' + \
               Notifications.footer()
        list_attachments = [('invoice.pdf', pdf_file, 'application/pdf')]

        EmailMessageThread.send_mail_with_attachments(from_email, to, body, subject, body_content_type,
                                                      list_attachments, True)

    @staticmethod
    def send_notification_for_breach_security():

        # Get all system emails
        email_system_configuration_list = ['', SystemConfiguration.corporateEmail, SystemConfiguration.reportEmail]
        emails_users = User.objects.exclude(email__in=email_system_configuration_list) \
            .values_list('email', flat=True).distinct()

        for email in emails_users:
            from_email = 'Grooving <no-reply@grupogrooving.com>'
            to = [email]
            subject = 'Notice of data breach'
            body_content_type = 'html'
            body = '<p>We are writing to inform you about a data security issue that many involve ' \
                   'your Grooving account information. We have taken steps to secure your account ' \
                   'and are working closely with law enforcement.</p>' \
                   '<p>For security reasons, you must reset your password to protect your personal ' \
                   'information.</p>' + Notifications.footer()

            EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)

    @staticmethod
    def send_email_ban_unban_users(user_id):

        # Entity database objects (necessary from template & email)

        user = User.objects.filter(pk=user_id).first()
        system_configuration = SystemConfiguration.objects.filter(pk=1).first()

        # Email

        from_email = 'Grooving <no-reply@grupogrooving.com>'
        to = [user.email]
        body_content_type = 'html'

        if user.is_active:
            subject = 'Your Grooving account has been actived again'
            body = '<p>Hello,</p>' \
                   '<p>Thanks for contacting Grooving Support. We have activated your account again.</p>' \
                   '<p>We apologize for the inconvenience.</p>'
        else:
            subject = 'Your Grooving account has been banned'
            body = '<p>This account has been temporaly banned to a violation of ours Terms & conditions. Please ' \
                   'contact to Grooving support at ' + system_configuration.reportEmail + ' </p>'

        body += Notifications.footer()

        EmailMessageThread.send_mail(from_email, to, body, subject, body_content_type, True)
