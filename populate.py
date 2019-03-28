import os
import django
import random
import string
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Server.settings')
django.setup()
from Grooving.models import ArtisticGender, Portfolio, Artist, Zone, PortfolioModule, Calendar, PaymentPackage, \
    Performance, Fare, Custom, Offer, Customer, EventLocation, SystemConfiguration

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def _service_generate_unique_payment_code():
    random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    payment_code = random_alphanumeric
    return payment_code

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

    # Portfolios with his modules

    portfolio1 = Portfolio.objects.create(artisticName='Carlos DJ', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio1.artisticGender.add(artistic_gender2)
    portfolio1.zone.add(zone1)
    portfolio1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio1, description='It was a great festival')
    portfolio1_module1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio1, description='Video with Kill Clown', link='https://www.youtube.com/watch?v=BDhUtaS4GT8')
    portfolio1_module1.save()

    # ----

    portfolio2 = Portfolio.objects.create(artisticName='From the noise', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio2.artisticGender.add(artistic_gender4)
    portfolio2.zone.add(zone1)
    portfolio2.save()

    portfolio2_module1 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio2, link='https://www.facebook.com/fromthenoise/')
    portfolio2_module1.save()

    portfolio2_module2 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio2, link='https://www.facebook.com/batraciosvq/')
    portfolio2_module2.save()

    portfolio2_module3 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2, link='https://www.youtube.com/watch?v=CEaJ-COP9Rs')
    portfolio2_module3.save()

    portfolio2_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2, link='https://www.youtube.com/watch?v=g43nbmB1cD8')
    portfolio2_module4.save()


    # ----

    portfolio3 = Portfolio.objects.create(artisticName='Los saraos', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio3.artisticGender.add(artistic_gender5)
    portfolio3.zone.add(zone1)
    portfolio3.save()

    # ----

    portfolio4 = Portfolio.objects.create(artisticName='Ana DJ', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio4.zone.add(zone2)
    portfolio4.artisticGender.add(artistic_gender2)
    portfolio4.save()

    # ----

    portfolio5 = Portfolio.objects.create(artisticName='Pasando olimpicamente', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio5.artisticGender.add(artistic_gender8)
    portfolio5.zone.add(zone2)
    portfolio5.save()

    # ----

    portfolio6 = Portfolio.objects.create(artisticName='Una chirigota sin clase', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio6.artisticGender.add(artistic_gender8)
    portfolio6.zone.add(zone1)
    portfolio6.save()

    # ----

    portfolio7 = Portfolio.objects.create(artisticName='Batracio', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio7.artisticGender.add(artistic_gender3)
    portfolio7.artisticGender.add(artistic_gender4)
    portfolio7.zone.add(zone1)
    portfolio7.save()

    portfolio7_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio7, description='Group photo',
                                                        link='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/22089933_1594772467232483_3080874756432701823_n.jpg?_nc_cat=106&_nc_ht=scontent-mad1-1.xx&oh=def5d818429407165ba36763b4d352d6&oe=5D41A03B')
    portfolio7_module1.save()


    portfolio7_module2 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio7, description='Canal de Youtube',
                                                        link='https://www.youtube.com/channel/UC_SLV3MDv1LMdrg3hBITsTQ')
    portfolio7_module2.save()

    # ----

    portfolio8 = Portfolio.objects.create(artisticName='Medictum', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio8.artisticGender.add(artistic_gender3)
    portfolio8.artisticGender.add(artistic_gender4)
    portfolio8.zone.add(zone1)
    portfolio8.save()

    portfolio8_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8, description='New disc!!!',
                                                        link='http://medictum.es/wp-content/uploads/2016/09/portadaweb.jpg')
    portfolio8_module1.save()

    portfolio8_module2 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8, description='Antonio Medina',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-1.jpg')
    portfolio8_module2.save()

    portfolio8_module3 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8, description='Manuel Medina',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-2.jpg')
    portfolio8_module3.save()

    portfolio8_module4 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8, description='Rafael Córdoba',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-3.jpg')
    portfolio8_module4.save()

    portfolio8_module5 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8, description='Pablo Pérez',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-4.jpg')
    portfolio8_module5.save()

    portfolio8_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8, description='Medictum - El país de las pesadillas',
                                                        link='https://www.youtube.com/watch?v=EdUFDOM4lrU')
    portfolio8_module6.save()

    portfolio8_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8, description='Medictum - Sala Palo Palo',
                                                        link='https://www.youtube.com/watch?v=bgqfkpxH5h0')
    portfolio8_module7.save()

    portfolio8_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8, description='Medictum - Última oportunidad',
                                                        link='https://www.youtube.com/watch?v=fYzhR6g9J-4')
    portfolio8_module8.save()

    portfolio8_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8, description='Medictum - Última oportunidad',
                                                        link='https://www.youtube.com/watch?v=9wSTyCbDicE')
    portfolio8_module9.save()

    # ----

    portfolio9 = Portfolio.objects.create(artisticName='Waterdogs', banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg')
    portfolio9.artisticGender.add(artistic_gender3)
    portfolio9.artisticGender.add(artistic_gender4)
    portfolio9.zone.add(zone2)
    portfolio9.save()

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
    user8_artist8 = User.objects.create(username='artist8', password=make_password('artist8artist8'), first_name='Rafael', last_name='Córdoba', email='contacto@medictum.es')
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

    artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1, phone='600304999', photo='https://cdn.pixabay.com/photo/2016/02/19/11/36/microphone-1209816_1280.jpg')
    artist1.save()
    artist2 = Artist.objects.create(user=user2_artist2, portfolio=portfolio2, phone='695099812', photo='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/20953179_10155798140312625_5517808811547907373_n.jpg?_nc_cat=108&_nc_ht=scontent-mad1-1.xx&oh=78561ec93ba4604a3c5a570cbe101b40&oe=5D4D1ED1')
    artist2.save()
    artist3 = Artist.objects.create(user=user3_artist3, portfolio=portfolio3, phone='695990241', photo='https://cdn.pixabay.com/photo/2016/02/19/11/36/microphone-1209816_1280.jpg')
    artist3.save()
    artist4 = Artist.objects.create(user=user4_artist4, portfolio=portfolio4, phone='610750391', photo='https://cdn.pixabay.com/photo/2016/02/19/11/36/microphone-1209816_1280.jpg')
    artist4.save()
    artist5 = Artist.objects.create(user=user5_artist5, portfolio=portfolio5, phone='675181175', photo='https://cdn.pixabay.com/photo/2016/02/19/11/36/microphone-1209816_1280.jpg')
    artist5.save()
    artist6 = Artist.objects.create(user=user6_artist6, portfolio=portfolio6, phone='673049277', photo='https://unplatillodesal.files.wordpress.com/2017/12/pablo-delgado_a-2.jpg')
    artist6.save()
    artist7 = Artist.objects.create(user=user7_artist7, portfolio=portfolio7, phone='664196105', photo='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/50732294_2114221071976992_2173326934371467264_o.jpg?_nc_cat=100&_nc_ht=scontent-mad1-1.xx&oh=dacf068903a3703434b52cfade783470&oe=5D09C938')
    artist7.save()
    artist8 = Artist.objects.create(user=user8_artist8, portfolio=portfolio8, phone='664596466', photo='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-3.jpg')
    artist8.save()
    artist9 = Artist.objects.create(user=user9_artist9, portfolio=portfolio9, phone='679739257', photo='https://media.licdn.com/dms/image/C4E03AQFAONXIX44h6w/profile-displayphoto-shrink_800_800/0?e=1559174400&v=beta&t=eEhhR1sr9-p1fr1tREXmlXV6WAzPvNlFDHhlV8SNwRY')
    artist9.save()

    # Customers with credit card

    customer1 = Customer.objects.create(user=user10_customer1, phone='639154189', holder='Rafael Esquivias Ramírez', expirationDate='2020-10-01', number='4651001401188232', cvv='797')
    customer1.save()
    customer2 = Customer.objects.create(user=user11_customer2, phone='664656659', holder='Jorge Jiménez del Corral', expirationDate='2027-03-01', number='4934521448108546', cvv='675')
    customer2.save()
    customer3 = Customer.objects.create(user=user12_customer3, phone='678415820', holder='Juan Manuel Fernández', expirationDate='2025-10-01', number='4656508395720981', cvv='103')
    customer3.save()
    customer4 = Customer.objects.create(user=user13_customer4, phone='627322721', holder='Miguel Romero Gutierrez', expirationDate='2027-03-01', number='4826704855401486', cvv='616')
    customer4.save()

    # Event location

    event_location1 = EventLocation.objects.create(name='Event 1 - Festival Rockupo', address='Universidad Pablo de Olavide', equipment='Yes', zone=zone1, customer=customer1)
    event_location1.save()
    event_location2 = EventLocation.objects.create(name='Event 2 - La Posada Sevilla', address='C/Astronomía, 42, 41015', equipment='Yes', zone=zone1, customer=customer2)
    event_location2.save()
    event_location3 = EventLocation.objects.create(name='Event 3 - Rosalia en vivo', address='C/Sol, 45, 41652', equipment='Yes', zone=zone1, customer=customer3)
    event_location3.save()
    event_location4 = EventLocation.objects.create(name='Event 4 - Charlie XCX', address='C/Amalgama, 2, 41609', equipment='Yes', zone=zone2, customer=customer4)
    event_location4.save()

    # Payment packages with Payment types

    performance1_paymentPackage1 = Performance.objects.create(info='Performance Payment Type from Carlos DJ',
                                                              hours=1.5, price=50)
    performance1_paymentPackage1.save()

    paymentPackage1_performance1 = PaymentPackage.objects.create(description='Performance Payment Package Type from Carlos DJ',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance1_paymentPackage1)
    paymentPackage1_performance1.save()

    fare1_paymentPackage2 = Fare.objects.create(priceHour=45)
    fare1_paymentPackage2.save()

    paymentPackage2_fare1 = PaymentPackage.objects.create(description='Fare Payment Package Type from Carlos DJ',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare1_paymentPackage2)
    paymentPackage2_fare1.save()

    custom1_paymentPackage3 = Custom.objects.create(minimumPrice=60)
    custom1_paymentPackage3.save()

    paymentPackage3_custom1 = PaymentPackage.objects.create(description='Custom Payment Package Type from Carlos DJ',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom1_paymentPackage3)
    paymentPackage3_custom1.save()

    # ----

    performance2_paymentPackage4 = Performance.objects.create(info='Performance Payment Type from From the noise',
                                                              hours=1.5, price=50)
    performance2_paymentPackage4.save()

    paymentPackage4_performance2 = PaymentPackage.objects.create(description='Performance Payment Package Type from From the noise',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance2_paymentPackage4)
    paymentPackage4_performance2.save()

    fare2_paymentPackage5 = Fare.objects.create(priceHour=45)
    fare2_paymentPackage5.save()

    paymentPackage5_fare2 = PaymentPackage.objects.create(description='Fare Payment Package Type from From the noise',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare2_paymentPackage5)
    paymentPackage5_fare2.save()

    custom2_paymentPackage6 = Custom.objects.create(minimumPrice=60)
    custom2_paymentPackage6.save()

    paymentPackage6_custom2 = PaymentPackage.objects.create(description='Custom Payment Package Type from From the noise',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom2_paymentPackage6)
    paymentPackage6_custom2.save()

    # ----

    performance3_paymentPackage7 = Performance.objects.create(info='Performance Payment Type from Los saraos',
                                                              hours=1.5, price=50)
    performance3_paymentPackage7.save()

    paymentPackage7_performance3 = PaymentPackage.objects.create(description='Performance Payment Package Type from Los saraos',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance3_paymentPackage7)
    paymentPackage7_performance3.save()

    fare3_paymentPackage8 = Fare.objects.create(priceHour=45)
    fare3_paymentPackage8.save()

    paymentPackage8_fare3 = PaymentPackage.objects.create(description='Fare Payment Package Type from Los saraos',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare3_paymentPackage8)
    paymentPackage8_fare3.save()

    custom3_paymentPackage9 = Custom.objects.create(minimumPrice=60)
    custom3_paymentPackage9.save()

    paymentPackage9_custom3 = PaymentPackage.objects.create(description='Custom Payment Package Type from Los saraos',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom3_paymentPackage9)
    paymentPackage9_custom3.save()

    # ----

    performance4_paymentPackage10 = Performance.objects.create(info='Performance Payment Type from Ana DJ',
                                                              hours=1.5, price=50)
    performance4_paymentPackage10.save()

    paymentPackage10_performance4 = PaymentPackage.objects.create(description='Performance Payment Package Type from Ana DJ',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance4_paymentPackage10)
    paymentPackage10_performance4.save()

    fare4_paymentPackage11 = Fare.objects.create(priceHour=45)
    fare4_paymentPackage11.save()

    paymentPackage11_fare3 = PaymentPackage.objects.create(description='Fare Payment Package Type from Ana DJ',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare4_paymentPackage11)
    paymentPackage11_fare3.save()

    custom4_paymentPackage12 = Custom.objects.create(minimumPrice=60)
    custom4_paymentPackage12.save()

    paymentPackage12_custom4 = PaymentPackage.objects.create(description='Custom Payment Package Type from Ana DJ',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom4_paymentPackage12)
    paymentPackage12_custom4.save()

    # ----

    performance5_paymentPackage13 = Performance.objects.create(info='Performance Payment Type from Pasando olimpicamente',
                                                              hours=1.5, price=50)
    performance5_paymentPackage13.save()

    paymentPackage13_performance5 = PaymentPackage.objects.create(description='Performance Payment Package Type from Pasando olimpicamente',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance5_paymentPackage13)
    paymentPackage13_performance5.save()

    fare5_paymentPackage14 = Fare.objects.create(priceHour=45)
    fare5_paymentPackage14.save()

    paymentPackage14_fare5 = PaymentPackage.objects.create(description='Fare Payment Package Type from Pasando olimpicamente',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare5_paymentPackage14)
    paymentPackage14_fare5.save()

    custom5_paymentPackage15 = Custom.objects.create(minimumPrice=60)
    custom5_paymentPackage15.save()

    paymentPackage15_custom5 = PaymentPackage.objects.create(description='Custom Payment Package Type from Pasando olimpicamente',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom5_paymentPackage15)
    paymentPackage15_custom5.save()

    # ----

    performance6_paymentPackage16 = Performance.objects.create(info='Performance Payment Type from Una chirigota con clase',
                                                              hours=1.5, price=50)
    performance6_paymentPackage16.save()

    paymentPackage16_performance6 = PaymentPackage.objects.create(description='Performance Payment Package Type from Una chirigota con clase',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance6_paymentPackage16)
    paymentPackage16_performance6.save()

    fare6_paymentPackage17 = Fare.objects.create(priceHour=45)
    fare6_paymentPackage17.save()

    paymentPackage17_fare6 = PaymentPackage.objects.create(description='Fare Payment Package Type from Una chirigota con clase',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare6_paymentPackage17)
    paymentPackage17_fare6.save()

    custom6_paymentPackage18 = Custom.objects.create(minimumPrice=60)
    custom6_paymentPackage18.save()

    paymentPackage18_custom6 = PaymentPackage.objects.create(description='Custom Payment Package Type from Una chirigota con clase',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom6_paymentPackage18)
    paymentPackage18_custom6.save()

    # ----

    performance7_paymentPackage19 = Performance.objects.create(info='Performance Payment Type from Batracio',
                                                              hours=1.5, price=50)
    performance7_paymentPackage19.save()

    paymentPackage20_performance7 = PaymentPackage.objects.create(description='Performance Payment Package Type from Batracio',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance7_paymentPackage19)
    paymentPackage20_performance7.save()

    fare7_paymentPackage20 = Fare.objects.create(priceHour=45)
    fare7_paymentPackage20.save()

    paymentPackage20_fare7 = PaymentPackage.objects.create(description='Fare Payment Package Type from Batracio',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare7_paymentPackage20)
    paymentPackage20_fare7.save()

    custom7_paymentPackage21 = Custom.objects.create(minimumPrice=60)
    custom7_paymentPackage21.save()

    paymentPackage21_custom7 = PaymentPackage.objects.create(description='Custom Payment Package Type from Batracio',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom7_paymentPackage21)
    paymentPackage21_custom7.save()

    # ----

    performance8_paymentPackage22 = Performance.objects.create(info='Performance Payment Type from Medictum',
                                                              hours=1.5, price=50)
    performance8_paymentPackage22.save()

    paymentPackage22_performance8 = PaymentPackage.objects.create(description='Performance Payment Package Type from Medictum',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance8_paymentPackage22)
    paymentPackage22_performance8.save()

    fare8_paymentPackage23 = Fare.objects.create(priceHour=45)
    fare8_paymentPackage23.save()

    paymentPackage23_fare8 = PaymentPackage.objects.create(description='Fare Payment Package Type from Medictum',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare8_paymentPackage23)
    paymentPackage23_fare8.save()

    custom8_paymentPackage24 = Custom.objects.create(minimumPrice=60)
    custom8_paymentPackage24.save()

    paymentPackage24_custom8 = PaymentPackage.objects.create(description='Custom Payment Package Type from Medictum',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom8_paymentPackage24)
    paymentPackage24_custom8.save()

    # ----

    performance9_paymentPackage25 = Performance.objects.create(info='Performance Payment Type from Waterdogs',
                                                              hours=1.5, price=50)
    performance9_paymentPackage25.save()

    paymentPackage25_performance9 = PaymentPackage.objects.create(description='Performance Payment Package Type from Waterdogs',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                performance=performance9_paymentPackage25)
    paymentPackage25_performance9.save()

    fare9_paymentPackage26 = Fare.objects.create(priceHour=45)
    fare9_paymentPackage26.save()

    paymentPackage26_fare9 = PaymentPackage.objects.create(description='Fare Payment Package Type from Waterdogs',
                                                                appliedVAT=21, portfolio=portfolio1,
                                                                fare=fare9_paymentPackage26)
    paymentPackage26_fare9.save()

    custom9_paymentPackage27 = Custom.objects.create(minimumPrice=60)
    custom9_paymentPackage27.save()

    paymentPackage27_custom9 = PaymentPackage.objects.create(description='Custom Payment Package Type from Waterdogs',
                                                          appliedVAT=21, portfolio=portfolio1,
                                                          custom=custom9_paymentPackage27)
    paymentPackage27_custom9.save()


    # Offers

    offer1_performance1 = Offer.objects.create(description='Oferta 1 to Carlos DJ by performance', status='PENDING',
                                               date='2019-04-25 12:00:00', hours=2.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1)
    offer1_performance1.save()

    offer2_performance1 = Offer.objects.create(description='Oferta 2 to Carlos DJ by performance', status='NEGOTIATION',
                                               date='2019-07-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1)
    offer2_performance1.save()

    offer3_performance1 = Offer.objects.create(description='Oferta 3 to Carlos DJ by performance', status='CANCELED',
                                               date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location2)
    offer3_performance1.save()

    offer4_fare1 = Offer.objects.create(description='Oferta 4 to Carlos DJ by fare', status='PENDING',
                                               date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage2_fare1,
                                               eventLocation=event_location2)
    offer4_fare1.save()

    offer5_custom1 = Offer.objects.create(description='Oferta 5 to Carlos DJ by custom', status='CONTRACT_MADE',
                                               date='2019-8-25 12:00:00', hours=1.5, price='115', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage3_custom1,
                                               eventLocation=event_location1)
    offer5_custom1.save()

    offer6_custom1 = Offer.objects.create(description='Oferta 6 to Carlos DJ by custom', status='REJECTED',
                                               date='2019-10-25 19:00:00', hours=1.5, price='100', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage3_custom1,
                                               eventLocation=event_location1)
    offer6_custom1.save()

    offer7_performance2 = Offer.objects.create(description='Oferta 7 to From the noise by performance', status='REJECTED',
                                               date='2019-10-25 15:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage4_performance2,
                                               eventLocation=event_location1)
    offer7_performance2.save()

    offer9_fare2 = Offer.objects.create(description='Oferta 9 to From the noise by fare', status='CANCELLED',
                                               date='2019-03-27 00:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage5_fare2,
                                               eventLocation=event_location4)
    offer9_fare2.save()

    offer10_fare2 = Offer.objects.create(description='Oferta 10 to From the noise by performance', status='NEGOTIATION',
                                               date='2019-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage5_fare2,
                                               eventLocation=event_location4)
    offer10_fare2.save()

    offer11_custom2 = Offer.objects.create(description='Oferta 11 to From the noise by performance', status='NEGOTIATION',
                                               date='2019-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage5_fare2,
                                               eventLocation=event_location3)
    offer11_custom2.save()

    offer12_custom2 = Offer.objects.create(description='Oferta 12 to From the noise by performance', status='CANCELLED',
                                               date='2017-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               paymentPackage=paymentPackage5_fare2,
                                               eventLocation=event_location3)
    offer12_custom2.save()


save_data()
