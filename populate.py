import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()

from Grooving.models import ArtisticGender, Portfolio, Artist, Zone, PortfolioModule, Calendar, PaymentPackage, Performance, Fare, Custom, Offer, Customer, EventLocation, Offer, SystemConfiguration
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def delete_data():
    SystemConfiguration.objects.all().delete()
    Offer.objects.all().delete()
    User.objects.all().delete()
    Artist.objects.all().delete()
    Customer.objects.all().delete()
    EventLocation.objects.all().delete()
    Performance.objects.all().delete()
    Fare.objects.all().delete()
    Custom.objects.all().delete()
    PaymentPackage.objects.all().delete()
    ArtisticGender.objects.all().delete()
    Portfolio.objects.all().delete()
    Artist.objects.all().delete()
    Zone.objects.all().delete()
    PortfolioModule.objects.all().delete()
    Calendar.objects.all().delete()


def save_data():

    # System configuration
    system_configuration1 = SystemConfiguration.objects.create(minimumPrice='20', currency='EUR', paypalTax='2.9', creditCardTax='1.9',
                                                               vat='21', profit='7', corporateEmail='info@grooving.com',
                                                               reportEmail='report@grooving.com', appName='Grooving',
                                                               slogan='Connecting artist with you', termsText='Terms & conditions',
                                                               privacyText='Privacy text', logo='')
    system_configuration1.save()

    # ArtisticGenders

    artistic_gender1 = ArtisticGender.objects.create(name='Music')
    artistic_gender1.save()

    artistic_gender2 = ArtisticGender.objects.create(name='DJ', parentGender=artistic_gender1)
    artistic_gender2.save()

    artistic_gender3 = ArtisticGender.objects.create(name='Pop', parentGender=artistic_gender1)
    artistic_gender3.save()

    artistic_gender4 = ArtisticGender.objects.create(name='Rock', parentGender=artistic_gender1)
    artistic_gender4.save()

    artistic_gender5 = ArtisticGender.objects.create(name='Flamenco', parentGender=artistic_gender1)
    artistic_gender5.save()

    artistic_gender6 = ArtisticGender.objects.create(name='Magician')
    artistic_gender6.save()

    artistic_gender7 = ArtisticGender.objects.create(name='Comedian')
    artistic_gender7.save()

    artistic_gender8 = ArtisticGender.objects.create(name='Carnival')
    artistic_gender8.save()


    # Zones

    zone1 = Zone.objects.create(name='Sevilla')
    zone1.save()

    zone2 = Zone.objects.create(name='Mairena del Aljarafe', parentZone=zone1)
    zone2.save()

    zone3 = Zone.objects.create(name='Ecija', parentZone=zone1)
    zone3.save()

    zone4 = Zone.objects.create(name='Madrid')
    zone4.save()


    # Portfolios

    portfolio1 = Portfolio.objects.create(artisticName='Carlos DJ')
    portfolio1.artisticGender.add(artistic_gender2)
    portfolio1.zone.add(zone1)
    portfolio1.save()

    portfolio2 = Portfolio.objects.create(artisticName='From the noise')
    portfolio2.artisticGender.add(artistic_gender4)
    portfolio2.zone.add(zone1)
    portfolio2.save()

    portfolio3 = Portfolio.objects.create(artisticName='Los saraos')
    portfolio3.artisticGender.add(artistic_gender5)
    portfolio3.zone.add(zone1)
    portfolio3.save()

    portfolio4 = Portfolio.objects.create(artisticName='Ana DJ')
    portfolio4.zone.add(zone2)
    portfolio4.artisticGender.add(artistic_gender2)
    portfolio4.save()

    portfolio5 = Portfolio.objects.create(artisticName='Pasando olimpicamente')
    portfolio5.artisticGender.add(artistic_gender8)
    portfolio5.zone.add(zone2)
    portfolio5.save()

    portfolio6 = Portfolio.objects.create(artisticName='Una chirigota sin clase')
    portfolio6.artisticGender.add(artistic_gender8)
    portfolio6.zone.add(zone1)
    portfolio6.save()

    portfolio7 = Portfolio.objects.create(artisticName='Batracio')
    portfolio7.artisticGender.add(artistic_gender3)
    portfolio7.artisticGender.add(artistic_gender4)
    portfolio7.zone.add(zone1)
    portfolio7.save()

    portfolio8 = Portfolio.objects.create(artisticName='Medictum')
    portfolio8.artisticGender.add(artistic_gender3)
    portfolio8.artisticGender.add(artistic_gender4)
    portfolio8.zone.add(zone1)
    portfolio8.save()

    portfolio9 = Portfolio.objects.create(artisticName='Waterdogs')
    portfolio9.artisticGender.add(artistic_gender3)
    portfolio9.artisticGender.add(artistic_gender4)
    portfolio9.zone.add(zone2)
    portfolio9.save()

    # Porfolio modules

    portfolio1_module1 = PortfolioModule.objects.create(type='DESCRIPTION', portfolioModule=portfolio1, description='It was a great festival')
    portfolio1_module1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='VIDEO', portfolioModule=portfolio1, description='Video with Kill Clown', link='https://www.youtube.com/watch?v=BDhUtaS4GT8')
    portfolio1_module1.save()

    portfolio2_module1 = PortfolioModule.objects.create(type='SOCIAL', portfolioModule=portfolio2, link='https://www.facebook.com/fromthenoise/')
    portfolio2_module1.save()

    portfolio2_module2 = PortfolioModule.objects.create(type='VIDEO', portfolioModule=portfolio2, link='https://www.youtube.com/watch?v=CEaJ-COP9Rs')
    portfolio2_module2.save()


    # Calendar

    availableDays = [False]*365
    availableDays[50] = True
    availableDays[51] = True
    availableDays[52] = True
    availableDays[53] = True

    calendar1 = Calendar.objects.create(year=2018, days=availableDays, portfolio=portfolio1)
    calendar1.save()

    calendar2 = Calendar.objects.create(year=2019, days=availableDays, portfolio=portfolio1)
    calendar2.save()

    calendar3 = Calendar.objects.create(year=2018, days=availableDays, portfolio=portfolio2)
    calendar3.save()

    calendar4 = Calendar.objects.create(year=2019, days=availableDays, portfolio=portfolio2)
    calendar4.save()

    calendar5 = Calendar.objects.create(year=2018, days=availableDays, portfolio=portfolio3)
    calendar5.save()

    calendar6 = Calendar.objects.create(year=2019, days=availableDays, portfolio=portfolio3)
    calendar6.save()

    calendar7 = Calendar.objects.create(year=2018, days=availableDays, portfolio=portfolio4)
    calendar7.save()

    calendar8 = Calendar.objects.create(year=2019, days=availableDays, portfolio=portfolio4)
    calendar8.save()


    # Payment package with Payment types

    performance1 = Performance.objects.create(info='Performance Payment Type from Carlos DJ', hours=1.5, price=50)
    performance1.save()

    fare1 = Fare.objects.create(priceHour=45)
    fare1.save()

    custom1 = Custom.objects.create(minimumPrice=60)
    custom1.save()

    paymentPackage1 = PaymentPackage.objects.create(description='Payment package from Carlos DJ', appliedVAT=21,
                                                 portfolio=portfolio1, performance=performance1, fare=fare1,
                                                 custom=custom1)

    performance2 = Performance.objects.create(info='Performance Payment Type from From the noise', hours=1.5, price=50)
    performance2.save()

    fare2 = Fare.objects.create(priceHour=45)
    fare2.save()

    custom2 = Custom.objects.create(minimumPrice=60)
    custom2.save()

    paymentPackage2 = PaymentPackage.objects.create(description='Payment package from From the noise', appliedVAT=21,
                                                 portfolio=portfolio2, performance=performance2, fare=fare2,
                                                 custom=custom2)
    paymentPackage2.save()

    performance3 = Performance.objects.create(info='Performance Payment Type from Los saraos', hours=1.5, price=50)
    performance3.save()

    fare3 = Fare.objects.create(priceHour=45)
    fare3.save()

    custom3 = Custom.objects.create(minimumPrice=60)
    custom3.save()

    paymentPackage3 = PaymentPackage.objects.create(description='Payment package from Los saraos', appliedVAT=21,
                                                 portfolio=portfolio3, performance=performance3, fare=fare3,
                                                 custom=custom3)
    paymentPackage3.save()

    performance4 = Performance.objects.create(info='Performance Payment Type from Ana DJ', hours=1.5, price=50)
    performance4.save()

    fare4 = Fare.objects.create(priceHour=45)
    fare4.save()

    custom4 = Custom.objects.create(minimumPrice=60)
    custom4.save()

    paymentPackage4 = PaymentPackage.objects.create(description='Payment package from Ana DJ', appliedVAT=21,
                                                 portfolio=portfolio4, performance=performance4, fare=fare4,
                                                 custom=custom4)
    paymentPackage4.save()

    performance5 = Performance.objects.create(info='Performance Payment Type from Pasando olimpicamente', hours=1.5, price=50)
    performance5.save()

    fare5 = Fare.objects.create(priceHour=45)
    fare5.save()

    custom5 = Custom.objects.create(minimumPrice=60)
    custom5.save()

    paymentPackage5 = PaymentPackage.objects.create(description='Payment package from Pasando olimpicamente', appliedVAT=21,
                                                 portfolio=portfolio5, performance=performance5, fare=fare5,
                                                 custom=custom5)
    paymentPackage5.save()

    performance6 = Performance.objects.create(info='Performance Payment Type from Una chirigota con clase', hours=1.5, price=50)
    performance6.save()

    fare6 = Fare.objects.create(priceHour=45)
    fare6.save()

    custom6 = Custom.objects.create(minimumPrice=60)
    custom6.save()

    paymentPackage6 = PaymentPackage.objects.create(description='Payment package from Una chirigota con clase', appliedVAT=21,
                                                 portfolio=portfolio6, performance=performance6, fare=fare6,
                                                 custom=custom6)
    paymentPackage6.save()

    performance7 = Performance.objects.create(info='Performance Payment Type from Batracio', hours=1.5, price=50)
    performance7.save()

    fare7 = Fare.objects.create(priceHour=45)
    fare7.save()

    custom7 = Custom.objects.create(minimumPrice=60)
    custom7.save()

    paymentPackage7 = PaymentPackage.objects.create(description='Payment package from Batracio', appliedVAT=21,
                                                 portfolio=portfolio7, performance=performance7, fare=fare7,
                                                 custom=custom7)
    paymentPackage7.save()

    performance8 = Performance.objects.create(info='Performance Payment Type from Una chirigota con clase', hours=1.5, price=50)
    performance8.save()

    fare8 = Fare.objects.create(priceHour=45)
    fare8.save()

    custom8 = Custom.objects.create(minimumPrice=60)
    custom8.save()

    paymentPackage8 = PaymentPackage.objects.create(description='Payment package from Medictum', appliedVAT=21,
                                                 portfolio=portfolio8, performance=performance8, fare=fare8,
                                                 custom=custom8)
    paymentPackage8.save()

    performance9 = Performance.objects.create(info='Performance Payment Type from Waterdogs', hours=1.5, price=50)
    performance9.save()

    fare9 = Fare.objects.create(priceHour=45)
    fare9.save()

    custom9 = Custom.objects.create(minimumPrice=60)
    custom9.save()

    paymentPackage9 = PaymentPackage.objects.create(description='Payment package from Waterdogs', appliedVAT=21,
                                                 portfolio=portfolio9, performance=performance9, fare=fare9,
                                                 custom=custom9)
    paymentPackage9.save()


    # Event location

    event_location1 = EventLocation.objects.create(name='Event 1 - Festival Rockupo', address='Universidad Pablo de Olavide', equipment='Yes', zone=zone1)
    event_location1.save()
    event_location2 = EventLocation.objects.create(name='Event 2 - La Posada Sevilla', address='C/Astronomía, 42, 41015', equipment='Yes', zone=zone1)
    event_location2.save()
    event_location3 = EventLocation.objects.create(name='Event 3 - Rosalia en vivo', address='C/Sol, 45, 41652', equipment='Yes', zone=zone1)
    event_location3.save()
    event_location4 = EventLocation.objects.create(name='Event 4 - Charlie XCX', address='C/Amalgama, 2, 41609', equipment='Yes', zone=zone2)
    event_location4.save()

    # Users...

    # ,,,musician

    user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'), first_name='Carlos', last_name='Campos Cuesta', email='infoaudiowar@gmail.com')
    user1_artist1.save()
    user2_artist2 = User.objects.create(username='artist2', password=make_password('artist2artist2'), first_name='José Antonio', last_name='Granero Guzmán', email='josegraneroguzman@gmail.com')
    user2_artist2.save()
    user3_artist3 = User.objects.create(username='artist3', password=make_password('artist3artist3'), first_name='Francisco', last_name='Martín', email='saralcum@gmail.com')
    user3_artist3.save()
    user4_artist4 = User.objects.create(username='artist4', password=make_password('artist4artist4'), first_name='Ana', last_name='Mellado González', email='mellizalez@hotmail.com')
    user4_artist4.save()
    user5_artist5 = User.objects.create(username='artist5', password=make_password('artist5artist5'), first_name='Alejandro', last_name='Arteaga Ramírez', email='alejandroarteagaramirez@gmail.com')
    user5_artist5.save()
    user6_artist6 = User.objects.create(username='artist6', password=make_password('artist6artist6'), first_name='Pablo', last_name='Delgado Flores', email='pabloj.df@gmail.com')
    user6_artist6.save()
    user7_artist7 = User.objects.create(username='artist7', password=make_password('artist7artist7'), first_name='Domingo', last_name='Muñoz Daza', email='dmunnoz96@gmail.com')
    user7_artist7.save()
    user8_artist8 = User.objects.create(username='artist8', password=make_password('artist8artist8'), first_name='Rafael', last_name='Castillo Lobato', email='contacto@medictum.es')
    user8_artist8.save()
    user9_artist9 = User.objects.create(username='artist9', password=make_password('artist9artist9'), first_name='José Luis', last_name='Salvador Lauret', email='joseluis.salvador@gmail.com')
    user9_artist9.save()

    # ...customers

    user10_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'), first_name='Rafael', last_name='Esquivias Ramírez', email='resquiviasramirez@gmail.com')
    user10_customer1.save()
    user11_customer2 = User.objects.create(username='customer2', password=make_password('customer2customer2'), first_name='Jorge', last_name='Jimenez', email='jorjicorral@gmail.com')
    user11_customer2.save()
    user12_customer3 = User.objects.create(username='customer3', password=make_password('customer3customer3'), first_name='Juan Manuel', last_name='Fernández', email='surlive@imgempresas.com')
    user12_customer3.save()
    user13_customer4 = User.objects.create(username='customer4', password=make_password('customer4customer4'), first_name='Miguel', last_name='Romero Gutierrez') # La posada Sevilla
    user13_customer4.save()

    # ...admins

    user14_admin = User.objects.create(username='admin', password=make_password('admin'), is_staff=True, is_superuser=True)
    user14_admin.save()

    # Artists

    artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999')
    artist1.save()
    artist2 = Artist.objects.create(user=user2_artist2, portfolio=portfolio2, phone='695099812')
    artist2.save()
    artist3 = Artist.objects.create(user=user3_artist3, portfolio=portfolio3, phone='695990241')
    artist3.save()
    artist4 = Artist.objects.create(user=user4_artist4, portfolio=portfolio4, phone='610750391')
    artist4.save()
    artist5 = Artist.objects.create(user=user5_artist5, portfolio=portfolio5, phone='675181175')
    artist5.save()
    artist6 = Artist.objects.create(user=user6_artist6, portfolio=portfolio6, phone='673049277')
    artist6.save()
    artist7 = Artist.objects.create(user=user7_artist7, portfolio=portfolio7, phone='664196105')
    artist7.save()
    artist8 = Artist.objects.create(user=user8_artist8, portfolio=portfolio8, phone='664596466')
    artist8.save()
    artist9 = Artist.objects.create(user=user9_artist9, portfolio=portfolio9, phone='679739257')
    artist9.save()

    # Customers with credit card

    customer1 = Customer.objects.create(user=user10_customer1, phone='639154189', holder='Rafael Esquivias Ramírez', expirationDate='2020-10-01', number='4651001401188232', cvv='797', eventLocation=event_location1)
    customer1.save()
    customer2 = Customer.objects.create(user=user11_customer2, phone='664656659', holder='Jorge Jiménez del Corral', expirationDate='2027-03-01', number='4934521448108546', cvv='675', eventLocation=event_location2)
    customer2.save()
    customer3 = Customer.objects.create(user=user12_customer3, phone='678415820', holder='Juan Manuel Fernández', expirationDate='2025-10-01', number='4656508395720981', cvv='103', eventLocation=event_location3)
    customer3.save()
    customer4 = Customer.objects.create(user=user13_customer4, phone='627322721', holder='Miguel Romero Gutierrez', expirationDate='2027-03-01', number='4826704855401486', cvv='616', eventLocation=event_location4)
    customer4.save()

    # Offers

    offer1 = Offer.objects.create(description='Oferta 1', status='PENDING', date='2019-04-25 12:00:00', hours=2.5,
                                  price='120', currency='EUR', paymentCode='59558462', paymentPackage=paymentPackage1,
                                  eventLocation=event_location1)
    offer1.save()

    offer2 = Offer.objects.create(description='Oferta 2', status='NEGOCIATION', date='2019-08-14 12:00:00', hours=2.5,
                                  price='110', currency='EUR', paymentCode='59551262', paymentPackage=paymentPackage1,
                                  eventLocation=event_location1)
    offer2.save()

    offer3 = Offer.objects.create(description='Oferta 3', status='CONTRACT_MADE', date='2019-08-14 12:00:00', hours=2.5,
                                  price='160', currency='EUR', paymentCode='59158462', paymentPackage=paymentPackage1,
                                  eventLocation=event_location1)

    offer3.save()

    offer4 = Offer.objects.create(description='Oferta 4', status='WITHDRAWN', date='2019-09-01 12:00:00', hours=2.5,
                                  price='175', currency='EUR', paymentCode='59558478', paymentPackage=paymentPackage2,
                                  eventLocation=event_location2)
    offer4.save()

    offer5 = Offer.objects.create(description='Oferta 5', status='REJECTED', date='2019-04-28 12:00:00', hours=1.5,
                                  price='105', currency='EUR', paymentCode='59214292', paymentPackage=paymentPackage3,
                                  eventLocation=event_location2)
    offer5.save()

    offer6 = Offer.objects.create(description='Oferta 6', status='CANCELLED', date='2019-04-12 12:00:00', hours=3.5,
                                  price='75', currency='EUR', paymentCode='59553292', paymentPackage=paymentPackage3,
                                  eventLocation=event_location3)
    offer6.save()

    offer7 = Offer.objects.create(description='Oferta 7', status='CANCELLED', date='2019-08-24 12:00:00', hours=1.5,
                                  price='97', currency='EUR', paymentCode='59523292', paymentPackage=paymentPackage3,
                                  eventLocation=event_location3)
    offer7.save()

    offer8 = Offer.objects.create(description='Oferta 8', status='PAYMENT_MADE', date='2019-11-12 12:00:00', hours=1.5,
                                  price='97', currency='EUR', paymentCode='59558332', paymentPackage=paymentPackage3,
                                  eventLocation=event_location3)
    offer8.save()

    offer9 = Offer.objects.create(description='Oferta 9', status='CANCELLED', date='2019-04-12 12:00:00', hours=3.5,
                                  price='75', currency='EUR', paymentCode='59553291', paymentPackage=paymentPackage3,
                                  eventLocation=event_location3)
    offer9.save()

    offer10 = Offer.objects.create(description='Oferta 10', status='CANCELLED', date='2019-08-24 12:00:00', hours=1.5,
                                  price='97', currency='EUR', paymentCode='59523290', paymentPackage=paymentPackage4,
                                  eventLocation=event_location3)
    offer10.save()

    offer11 = Offer.objects.create(description='Oferta 11', status='PAYMENT_MADE', date='2019-11-12 12:00:00', hours=1.5,
                                  price='97', currency='EUR', paymentCode='51238339', paymentPackage=paymentPackage3,
                                  eventLocation=event_location3)
    offer11.save()

    offer12 = Offer.objects.create(description='Oferta 12', status='CANCELLED', date='2019-08-24 12:00:00', hours=1.5,
                                  price='97', currency='EUR', paymentCode='59756290', paymentPackage=paymentPackage4,
                                  eventLocation=event_location3)
    offer12.save()

    offer13 = Offer.objects.create(description='Oferta 13', status='PENDING', date='2020-11-12 12:00:00', hours=1.5,
                                  price='97', currency='EUR', paymentCode='59318339', paymentPackage=paymentPackage4,
                                  eventLocation=event_location3)
    offer13.save()


delete_data()
save_data()

