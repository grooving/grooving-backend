import os
import django
import random
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'Server.settings')
django.setup()

from Grooving.models import ArtisticGender, Portfolio, Artist, Zone, PortfolioModule, Calendar, PaymentPackage, \
    Performance, Fare, Custom, Offer, Customer, EventLocation, SystemConfiguration, Rating, Transaction

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password



def _service_generate_unique_payment_code():
    random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    payment_code = random_alphanumeric
    return payment_code


def save_data():
    # System configuration
    system_configuration1 = SystemConfiguration.objects.create(minimumPrice='20', currency='EUR', paypalTax='2.9',
                                                               creditCardTax='1.9',
                                                               vat='21', profit='7',
                                                               corporateEmail='grupogrooving@gmail.com',
                                                               reportEmail='grupogrooving@gmail.com',
                                                               appName='Grooving',
                                                               slogan='Connecting artist with you',
                                                               termsText='Terms & conditions',
                                                               privacyText='Privacy text', logo='')
    system_configuration1.save()

    # ArtisticGenders
    artistic_gender0 = ArtisticGender.objects.create(name='All genres')
    artistic_gender0.save()

    artistic_gender1 = ArtisticGender.objects.create(name='Music', parentGender=artistic_gender0)
    artistic_gender1.save()

    artistic_gender2 = ArtisticGender.objects.create(name='DJ', parentGender=artistic_gender1)
    artistic_gender2.save()

    artistic_gender3 = ArtisticGender.objects.create(name='Pop', parentGender=artistic_gender1)
    artistic_gender3.save()

    artistic_gender4 = ArtisticGender.objects.create(name='Rock', parentGender=artistic_gender1)
    artistic_gender4.save()

    artistic_gender5 = ArtisticGender.objects.create(name='Flamenco', parentGender=artistic_gender1)
    artistic_gender5.save()

    artistic_gender6 = ArtisticGender.objects.create(name='Magician', parentGender=artistic_gender0)
    artistic_gender6.save()

    artistic_gender7 = ArtisticGender.objects.create(name='Comedian', parentGender=artistic_gender0)
    artistic_gender7.save()

    artistic_gender8 = ArtisticGender.objects.create(name='Carnival', parentGender=artistic_gender0)
    artistic_gender8.save()

    artistic_gender9 = ArtisticGender.objects.create(name='Clowns', parentGender=artistic_gender7)
    artistic_gender9.save()

    artistic_gender11 = ArtisticGender.objects.create(name='Mariachis', parentGender=artistic_gender1)
    artistic_gender11.save()

    artistic_gender12 = ArtisticGender.objects.create(name='Animation', parentGender=artistic_gender0)
    artistic_gender12.save()

    artistic_gender13 = ArtisticGender.objects.create(name='Theater', parentGender=artistic_gender0)
    artistic_gender13.save()

    artistic_gender10 = ArtisticGender.objects.create(name='Drag Queen', parentGender=artistic_gender12)
    artistic_gender10.save()
    # Zones

    zone0 = Zone.objects.create(name='España')
    zone0.save()

    # comunidades
    zone1_0 = Zone.objects.create(name='Andalucía', parentZone=zone0)
    zone1_0.save()

    zone1_1 = Zone.objects.create(name='Castilla-La Mancha', parentZone=zone0)
    zone1_1.save()

    zone1_2 = Zone.objects.create(name='Región de Murcia', parentZone=zone0)
    zone1_2.save()

    zone1_3 = Zone.objects.create(name='Comunidad Valenciana', parentZone=zone0)
    zone1_3.save()

    zone1_4 = Zone.objects.create(name='Islas Baleares', parentZone=zone0)
    zone1_4.save()

    zone1_4 = Zone.objects.create(name='Cataluña', parentZone=zone0)
    zone1_4.save()

    zone1_5 = Zone.objects.create(name='Aragón', parentZone=zone0)
    zone1_5.save()

    zone1_6 = Zone.objects.create(name='Navarra', parentZone=zone0)
    zone1_6.save()

    zone1_7 = Zone.objects.create(name='La Rioja', parentZone=zone0)
    zone1_7.save()

    zone1_8 = Zone.objects.create(name='País Vasco', parentZone=zone0)
    zone1_8.save()

    zone1_9 = Zone.objects.create(name='Cantabria', parentZone=zone0)
    zone1_9.save()

    zone1_10 = Zone.objects.create(name='Asturias', parentZone=zone0)
    zone1_10.save()

    zone1_11 = Zone.objects.create(name='Galicia', parentZone=zone0)
    zone1_11.save()

    zone1_12 = Zone.objects.create(name='Castilla y León', parentZone=zone0)
    zone1_12.save()

    zone1_13 = Zone.objects.create(name='Comunidad de Madrid', parentZone=zone0)
    zone1_13.save()

    zone1_14 = Zone.objects.create(name='Canarias', parentZone=zone0)
    zone1_14.save()

    zone1_15 = Zone.objects.create(name='Ceuta', parentZone=zone0)
    zone1_15.save()

    zone1_16 = Zone.objects.create(name='Melilla', parentZone=zone0)
    zone1_16.save()

    zone1_17 = Zone.objects.create(name='Extremadura', parentZone=zone0)
    zone1_17.save()

    # Andalucía
    zone2 = Zone.objects.create(name='Sevilla', parentZone=zone1_0)
    zone2.save()

    zone3 = Zone.objects.create(name='Huelva', parentZone=zone1_0)
    zone3.save()

    zone4 = Zone.objects.create(name='Almería', parentZone=zone1_0)
    zone4.save()

    zone5 = Zone.objects.create(name='Cádiz', parentZone=zone1_0)
    zone5.save()

    zone6 = Zone.objects.create(name='Málaga', parentZone=zone1_0)
    zone6.save()

    zone7 = Zone.objects.create(name='Córdoba', parentZone=zone1_0)
    zone7.save()

    zone8 = Zone.objects.create(name='Granada', parentZone=zone1_0)
    zone8.save()

    zone9 = Zone.objects.create(name='Jaén', parentZone=zone1_0)
    zone9.save()

    # Aragón
    zone10 = Zone.objects.create(name='Huesca', parentZone=zone1_5)
    zone10.save()

    zone11 = Zone.objects.create(name='Teruel', parentZone=zone1_5)
    zone11.save()

    zone12 = Zone.objects.create(name='Zaragoza', parentZone=zone1_5)
    zone12.save()

    # Canarias

    zone13 = Zone.objects.create(name='Las Palmas', parentZone=zone1_14)
    zone13.save()

    zone14 = Zone.objects.create(name='Santa Cruz de Tenerife', parentZone=zone1_14)
    zone14.save()

    # Castilla y León
    zone15 = Zone.objects.create(name='Ávila', parentZone=zone1_12)
    zone15.save()

    zone16 = Zone.objects.create(name='Burgos', parentZone=zone1_12)
    zone16.save()

    zone17 = Zone.objects.create(name='León', parentZone=zone1_12)
    zone17.save()

    zone18 = Zone.objects.create(name='Palencia', parentZone=zone1_12)
    zone18.save()

    zone19 = Zone.objects.create(name='Salamanca', parentZone=zone1_12)
    zone19.save()

    zone20 = Zone.objects.create(name='Segovia', parentZone=zone1_12)
    zone20.save()

    zone21 = Zone.objects.create(name='Soria', parentZone=zone1_12)
    zone21.save()

    zone22 = Zone.objects.create(name='Valladolid', parentZone=zone1_12)
    zone22.save()

    zone23 = Zone.objects.create(name='Zamora', parentZone=zone1_12)
    zone23.save()

    # Castilla-La Mancha
    zone24 = Zone.objects.create(name='Albacete', parentZone=zone1_1)
    zone24.save()

    zone25 = Zone.objects.create(name='Ciudad Real', parentZone=zone1_1)
    zone25.save()

    zone26 = Zone.objects.create(name='Cuenca', parentZone=zone1_1)
    zone26.save()

    zone27 = Zone.objects.create(name='Guadalajara', parentZone=zone1_1)
    zone27.save()

    zone28 = Zone.objects.create(name='Toledo', parentZone=zone1_1)
    zone28.save()

    # Cataluña
    zone29 = Zone.objects.create(name='Barcelona', parentZone=zone1_4)
    zone29.save()

    zone30 = Zone.objects.create(name='Girona', parentZone=zone1_4)
    zone30.save()

    zone31 = Zone.objects.create(name='Lleida', parentZone=zone1_4)
    zone31.save()

    zone32 = Zone.objects.create(name='Tarragona', parentZone=zone1_4)
    zone32.save()

    # Valencia
    zone33 = Zone.objects.create(name='Alicante', parentZone=zone1_3)
    zone33.save()

    zone34 = Zone.objects.create(name='Castellón', parentZone=zone1_3)
    zone34.save()

    zone35 = Zone.objects.create(name='Valencia', parentZone=zone1_3)
    zone35.save()

    # Extremadura
    zone36 = Zone.objects.create(name='Badajoz', parentZone=zone1_17)
    zone36.save()

    zone37 = Zone.objects.create(name='Cáceres', parentZone=zone1_17)
    zone37.save()

    # Galicia
    zone38 = Zone.objects.create(name='A Coruña', parentZone=zone1_11)
    zone38.save()

    zone39 = Zone.objects.create(name='Lugo', parentZone=zone1_11)
    zone39.save()

    zone40 = Zone.objects.create(name='Ourense', parentZone=zone1_11)
    zone40.save()

    zone41 = Zone.objects.create(name='Pontevedra', parentZone=zone1_11)
    zone41.save()

    # País vasco
    zone42 = Zone.objects.create(name='Álava', parentZone=zone1_8)
    zone42.save()

    zone43 = Zone.objects.create(name='Guipuzkoa', parentZone=zone1_8)
    zone43.save()

    zone44 = Zone.objects.create(name='Bizkaia', parentZone=zone1_8)
    zone44.save()

    # Famous artist
    # TAMTA
    portfolio10 = Portfolio.objects.create(artisticName='Tamta',
                                           banner='http://www.ddi.com.au/wp-content/uploads/AdobeStock_115567415.jpeg',
                                           biography='Tamta, is a Georgian-Greek singer. She first achieved popularity in Greece and Cyprus in 2004 for her participation in Super Idol Greece, in which she placed second. She went on to release several charting albums and singles in Greece and Cyprus. Goduadze became a mentor on X Factor Georgia in 2014, and The X Factor Greece in 2016.')

    portfolio10.artisticGender.add(artistic_gender1)
    portfolio10.zone.add(zone0)
    portfolio10.save()

    portfolio10.artisticGender.add(artistic_gender3)
    portfolio10.zone.add(zone0)
    portfolio10.save()

    portfolio10_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Tv show',
                                                         link='https://www.formulatv.com/images/articulos/87000/n87271_n8ovm0YsatFie16RUc3HLxg49PEJzkB75-q.jpg')
    portfolio10_module1.save()

    portfolio10_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Spot show',
                                                         link='https://images.immediate.co.uk/volatile/sites/3/2019/02/Screen-Shot-2019-02-20-at-10.45.50-3a87e66.png?quality=45&resize=620,413')
    portfolio10_module2.save()

    portfolio10_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Show',
                                                         link='https://cyprus-mail.com/wp-content/uploads/2018/12/tamtaweb-770x571.jpg')
    portfolio10_module3.save()

    portfolio10_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='Videoclip',
                                                         link='https://66.media.tumblr.com/94d8c94bcdf538e4316bd59112911141/tumblr_pnye731raA1vzbee3o4_500.gif')
    portfolio10_module4.save()

    portfolio10_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio10,
                                                         description='New clip',
                                                         link='https://www.esc-plus.com/wp-content/uploads/2015/06/tamta-unloved-video-mikrofwno.jpg')
    portfolio10_module5.save()

    portfolio10_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Replay',
                                                         link='https://www.youtube.com/watch?v=ESkhPXfl4A0')
    portfolio10_module6.save()

    portfolio10_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Πες Μου Αν Τολμάς',
                                                         link='https://www.youtube.com/watch?v=LiD1kiUF9CQ')
    portfolio10_module7.save()

    portfolio10_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Tag You In My Sky',
                                                         link='https://www.youtube.com/watch?v=9G7FMG1ar1w')
    portfolio10_module8.save()

    portfolio10_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio10,
                                                         description='Don’t Kiss Goodbye',
                                                         link='https://www.youtube.com/watch?v=S3BagUEA-LU')
    portfolio10_module9.save()

    availableDays10 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar10 = Calendar.objects.create(days=availableDays10, portfolio=portfolio10)
    calendar10.save()

    user1_artist10 = User.objects.create(username='tamta', password=make_password('tamta'), first_name='Tamta',
                                         last_name='Goduadze', email='Joseph.jmlc@gmail.com')
    user1_artist10.save()

    artist10 = Artist.objects.create(user=user1_artist10, rating=5.0, portfolio=portfolio10, phone='600304999',
                                     photo='https://img.discogs.com/jgyNBtPsY4DiLegwMrOC9N_yOc4=/600x600/smart/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/A-1452461-1423476836-6354.jpeg.jpg',
                                     iban='ES6621000418401234567891')
    artist10.save()

    performance1_paymentPackageFamous1 = Performance.objects.create(info='This is only mi pay for mi top 8 songs',
                                                                    hours=1.5, price=200000)
    performance1_paymentPackageFamous1.save()

    paymentPackage1_performanceFamous1 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Tamta',
        portfolio=portfolio10,
        performance=performance1_paymentPackageFamous1)
    paymentPackage1_performanceFamous1.save()

    fare1_paymentPackageFamous1 = Fare.objects.create(priceHour=50000)

    fare1_paymentPackageFamous1.save()

    paymentPackage2_fareFamous1 = PaymentPackage.objects.create(description='Fare Payment Package Type from Tamta',
                                                                portfolio=portfolio10,
                                                                fare=fare1_paymentPackageFamous1)
    paymentPackage2_fareFamous1.save()

    custom1_paymentPackageFamous1 = Custom.objects.create(minimumPrice=50000)
    custom1_paymentPackageFamous1.save()

    paymentPackage3_customFamous1 = PaymentPackage.objects.create(description='Custom Payment Package Type from Tamta',
                                                                  portfolio=portfolio10,
                                                                  custom=custom1_paymentPackageFamous1)
    paymentPackage3_customFamous1.save()

    # Rosalia
    portfolio11 = Portfolio.objects.create(artisticName='Rosalía',
                                           banner='https://rosalia.com/11.de617e41.jpg',
                                           biography='She is a Spanish singer and actress. In 2018 she became the most Latin Grammy Award winning Spaniard for a single work. Her song "Malamente" won two awards out of five nominations.')

    portfolio11.artisticGender.add(artistic_gender1)
    portfolio11.zone.add(zone0)
    portfolio11.save()

    portfolio11.artisticGender.add(artistic_gender3)
    portfolio11.zone.add(zone0)
    portfolio11.save()

    portfolio11.artisticGender.add(artistic_gender5)
    portfolio11.zone.add(zone0)
    portfolio11.save()

    portfolio11_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Interview',
                                                         link='https://www.elindependiente.com/wp-content/uploads/2018/12/rosalia-efe2-1440x808.jpg')
    portfolio11_module1.save()

    portfolio11_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Billboard',
                                                         link='https://www.billboard.com/files/media/Rosalia-bb1-2019-feat-billboard-djhirpa-1548.jpg')
    portfolio11_module2.save()

    portfolio11_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Interview',
                                                         link='https://www.elindependiente.com/wp-content/uploads/2018/10/Rosalia-en-Nueva-York-1440x808.jpeg')
    portfolio11_module3.save()

    portfolio11_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Videoclip malamente',
                                                         link='https://i0.wp.com/revistafactum.com/wp-content/uploads/2018/11/Rosalia.gif?fit=640%2C360')
    portfolio11_module4.save()

    portfolio11_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio11,
                                                         description='Concert',
                                                         link='https://www.thenation.com/wp-content/uploads/2018/11/rosalia-ap-ba.jpg')
    portfolio11_module5.save()

    portfolio11_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='Con Altura',
                                                         link='https://www.youtube.com/watch?v=ESkhPXfl4A0')
    portfolio11_module6.save()

    portfolio11_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='MALAMENTE ',
                                                         link='https://www.youtube.com/watch?v=Rht7rBHuXW8')
    portfolio11_module7.save()

    portfolio11_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='DI MI NOMBRE',
                                                         link='https://www.youtube.com/watch?v=mUBMPaj0L3o')
    portfolio11_module8.save()

    portfolio11_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                         description='BAGDAD ',
                                                         link='https://www.youtube.com/watch?v=Q2WOIGyGzUQ')
    portfolio11_module9.save()

    portfolio11_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio11,
                                                          description='De Plata',
                                                          link='https://www.youtube.com/watch?v=NfDEEyg3AdA')
    portfolio11_module10.save()

    availableDays11 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar11 = Calendar.objects.create(days=availableDays11, portfolio=portfolio11)
    calendar11.save()

    user1_artist11 = User.objects.create(username='rosalia', password=make_password('rosalia'), first_name='Rosalía ',
                                         last_name='Vila Tobella', email='Joseph.jmlc@gmail.com')
    user1_artist11.save()

    artist11 = Artist.objects.create(user=user1_artist11, rating=5.0, portfolio=portfolio11, phone='600304999',
                                     photo='http://vein.es/wp-content/uploads/2018/11/cap5-lamento.gif',
                                     iban='ES6621000418401234567891')
    artist11.save()


    performance1_paymentPackageFamous2 = Performance.objects.create(info='I begin with mi new 7 songs and end with Malamente',
                                                              hours=2, price=500000)


    performance1_paymentPackageFamous2.save()

    paymentPackage1_performanceFamous2 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Rosalía',
        portfolio=portfolio11,
        performance=performance1_paymentPackageFamous2)
    paymentPackage1_performanceFamous2.save()


    fare1_paymentPackageFamous2 = Fare.objects.create(priceHour=100000)
    fare1_paymentPackageFamous2.save()

    paymentPackage2_fareFamous2 = PaymentPackage.objects.create(description='Fare Payment Package Type from Rosalía',
                                                          portfolio=portfolio11,
                                                          fare=fare1_paymentPackageFamous2)
    paymentPackage2_fareFamous2.save()

    custom1_paymentPackageFamous2 = Custom.objects.create(minimumPrice=100000)
    custom1_paymentPackageFamous2.save()

    paymentPackage3_customFamous2 = PaymentPackage.objects.create(description='Custom Payment Package Type from Rosalía',
                                                            portfolio=portfolio11,
                                                            custom=custom1_paymentPackageFamous2)
    paymentPackage3_customFamous2.save()


    # Taylor Swift
    portfolio12 = Portfolio.objects.create(artisticName='Taylor Swift',
                                           banner='http://img2.rtve.es/a/4429044?w=1600&preview=1516350190645.jpg',
                                           biography='Iis an American singer-songwriter. As one of the world`s leading contemporary recording artists, she is known for narrative songs about her personal life, which has received widespread media coverage.')

    portfolio12.artisticGender.add(artistic_gender1)
    portfolio12.zone.add(zone0)
    portfolio12.save()

    portfolio12.artisticGender.add(artistic_gender3)
    portfolio12.zone.add(zone0)
    portfolio12.save()

    portfolio12_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Paper',
                                                         link='https://www.eluniversal.com.mx/sites/default/files/2015/07/22/taylor-swift-sept2014-a06.jpg')
    portfolio12_module1.save()

    portfolio12_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Interview',
                                                         link='https://www.telemundo.com/sites/nbcutelemundo/files/styles/article_cover_image/public/images/gallery/2015/12/02/taylor-swift-sonriendo-1989-tour.jpg?itok=Hw4e6KN3')
    portfolio12_module2.save()

    '''
    portfolio12_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Smile',
                                                         link='https://em.wattpad.com/67028e42a9ebd5c53342cae98d2082deb0d12424/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f51387a68664f58415a73575937773d3d2d32372e313536343431653536393831363236393135363633353535333030392e676966?s=fit&w=720&h=720')
    portfolio12_module3.save()
    '''

    portfolio12_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Videoclip rainbow',
                                                         link='https://www.nacionrex.com/__export/1548185009356/sites/debate/img/2019/01/22/taylor_swift_cats_bombalurina_personaje_quien_es_foto_instagram_2019_crop1548184963929.jpg_1834093470.jpg')
    portfolio12_module4.save()

    portfolio12_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Concert',
                                                         link='https://ewedit.files.wordpress.com/2018/06/taylor-swift.jpg')
    portfolio12_module5.save()

    portfolio12_module6 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio12,
                                                         description='Interview',
                                                         link='http://reportajede.news/wp-content/uploads/2017/06/Taylor-Swift.jpg')
    portfolio12_module6.save()

    portfolio12_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                         description='Delicate ',
                                                         link='https://www.youtube.com/watch?v=tCXGJQYZ9JA')
    portfolio12_module7.save()

    portfolio12_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                         description='Ready For It',
                                                         link='https://www.youtube.com/watch?v=wIft-t-MQuE')
    portfolio12_module8.save()

    portfolio12_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                         description='Look What You Made Me Do',
                                                         link='https://www.youtube.com/watch?v=3tmd-ClpJxA')
    portfolio12_module9.save()

    portfolio12_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                          description='Wildest Dreams',
                                                          link='https://www.youtube.com/watch?v=IdneKLhsWOQ')
    portfolio12_module10.save()

    portfolio12_module11 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio12,
                                                          description='Style',
                                                          link='https://www.youtube.com/watch?v=-CmadmM5cOk')
    portfolio12_module11.save()

    availableDays12 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar12 = Calendar.objects.create(days=availableDays12, portfolio=portfolio12)
    calendar12.save()

    user1_artist12 = User.objects.create(username='taylor', password=make_password('taylor'),
                                         first_name='Taylor Alison ',
                                         last_name='Swift', email='Joseph.jmlc@gmail.com')
    user1_artist12.save()

    artist12 = Artist.objects.create(user=user1_artist12,rating=5.0, portfolio=portfolio12, phone='600304999',
                                     photo='https://los40es00.epimg.net/los40/imagenes/2018/08/18/actualidad/1534605895_686141_1534606292_noticia_normal.jpg',
                                     iban='ES6621000418401234567891')
    artist12.save()

    performance1_paymentPackageFamous3 = Performance.objects.create(
        info='I only play my songs of Reputation',
        hours=2, price=400000)

    performance1_paymentPackageFamous3.save()

    paymentPackage1_performanceFamous3 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from  Taylor Swift',
        portfolio=portfolio12,
        performance=performance1_paymentPackageFamous3)
    paymentPackage1_performanceFamous3.save()

    fare1_paymentPackageFamous3 = Fare.objects.create(priceHour=75000)
    fare1_paymentPackageFamous3.save()

    paymentPackage2_fareFamous3 = PaymentPackage.objects.create(description='Fare Payment Package Type from Taylor Swift',
                                                                portfolio=portfolio12,
                                                                fare=fare1_paymentPackageFamous3)
    paymentPackage2_fareFamous3.save()

    custom1_paymentPackageFamous3 = Custom.objects.create(minimumPrice=100000)
    custom1_paymentPackageFamous3.save()

    paymentPackage3_customFamous3 = PaymentPackage.objects.create(
        description='Custom Payment Package Type from Rosalía',
        portfolio=portfolio12,
        custom=custom1_paymentPackageFamous3)
    paymentPackage3_customFamous3.save()

    # Charli XCX
    portfolio13 = Portfolio.objects.create(artisticName='Charli XCX',
                                           banner='https://celebmix.com/wp-content/uploads/2018/07/charli-xcx-releases-two-of-her-best-singles-yet-focus-no-angel-01.jpg',
                                           biography='Iis an American singer-songwriter. As one of the world`s leading contemporary recording artists, she is known for narrative songs about her personal life, which has received widespread media coverage.')

    portfolio13.artisticGender.add(artistic_gender1)
    portfolio13.zone.add(zone0)
    portfolio13.save()

    portfolio13.artisticGender.add(artistic_gender3)
    portfolio13.zone.add(zone0)
    portfolio13.save()

    portfolio13_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Road',
                                                         link='https://www.musicmundial.com/wp-content/uploads/2018/02/charli-xcx.jpg')
    portfolio13_module1.save()

    portfolio13_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Paper',
                                                         link='https://static.stereogum.com/uploads/2018/05/charli-xcx-5-in-the-morning-1527704949-640x640.jpg')
    portfolio13_module2.save()

    portfolio13_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Old Profile',
                                                         link='https://pixel.nymag.com/imgs/daily/vulture/2018/08/03/magazine/03-charlie-xcx-feature-lede.w512.h600.2x.jpg')
    portfolio13_module3.save()

    portfolio13_module4 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Old style',
                                                         link='https://studiosol-a.akamaihd.net/uploadfile/letras/fotos/3/c/1/e/3c1ef403cef2e1dd5bf801b6efcfe4b9.jpg')
    portfolio13_module4.save()

    portfolio13_module5 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio13,
                                                         description='Concert',
                                                         link='https://ksassets.timeincuk.net/wp/uploads/sites/55/2018/07/charli-xcx-sucker-fake-920x584.jpg')
    portfolio13_module5.save()

    portfolio13_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                         description='Troye Sivan',
                                                         link='https://www.youtube.com/watch?v=6-v1b9waHWY')
    portfolio13_module7.save()

    portfolio13_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                         description='Girls Night Out',
                                                         link='https://www.youtube.com/watch?v=IFr3GnboNRU')
    portfolio13_module8.save()

    portfolio13_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                         description='Backseat ',
                                                         link='https://www.youtube.com/watch?v=hiGqKwy4yM0')
    portfolio13_module9.save()

    portfolio13_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio13,
                                                          description=' I Love It ',
                                                          link='https://www.youtube.com/watch?v=UxxajLWwzqY')
    portfolio13_module10.save()

    availableDays13 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                       '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar13 = Calendar.objects.create(days=availableDays13, portfolio=portfolio13)
    calendar13.save()

    user1_artist13 = User.objects.create(username='charli', password=make_password('charli'),
                                         first_name='Charlotte Emma',
                                         last_name='Aitchison', email='Joseph.jmlc@gmail.com')
    user1_artist13.save()

    artist13 = Artist.objects.create(user=user1_artist13,rating=5.0, portfolio=portfolio13, phone='600304999',
                                     photo='https://data.whicdn.com/images/152059660/original.gif',
                                     iban='ES6621000418401234567891')
    artist13.save()

    # Portfolios with his modules

    portfolio1 = Portfolio.objects.create(artisticName='Carlos DJ',
                                          banner='https://c.pxhere.com/photos/52/a5/mixer_sound_board_sound_studio_broadcasting_radio_djs_music-1371930.jpg!d',
                                          biography='Musician, producer, DJ, pianist, promoter, and electronic music enthusiast alike, David Michael hails out of Dayton, Ohio.  When not performing, he spends his time in the studio creating his own music… aided by over a decade of piano lessons and an upbringing in a very musically-influenced home.  Having spent many years playing at all of the major local night clubs (alongside local hard-hitters and national acts alike), holding multiple residencies, DJing special events and promoting his own shows, David has had a lot of time to develop his sound.  For him, it’s all about mood and a deep, hypnotic groove… playing those tracks that get you tapping your feet and nodding your head without you realizing it, regardless of genre, tempo, style, or release date. Don’t be surprised when you suddenly find yourself dancing')
    portfolio1.artisticGender.add(artistic_gender2)
    portfolio1.zone.add(zone2)
    portfolio1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio1,
                                                        description='It was a great festival',
                                                        link='https://www.youtube.com/watch?v=xAzWJCwZY6w')
    portfolio1_module1.save()

    portfolio1_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio1,
                                                        description='Video with Kill Clown',
                                                        link='https://www.youtube.com/watch?v=BDhUtaS4GT8')
    portfolio1_module1.save()

    # ----

    portfolio2 = Portfolio.objects.create(artisticName='From the noise',
                                          banner='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/1377395_756950037692403_4684275136466205538_n.jpg?_nc_cat=107&_nc_ht=scontent-mad1-1.xx&oh=452afbe02d9696047bad6af696ed1276&oe=5D47A9C6',
                                          biography='Somos un grupo de Sevilla, formado el 2010, somos 6 componentes y tocamos un estilo muy alternativo que mezcla hip hop con rock, electrónica y metal. Tenemos melodías y letras contudentes. Estamos bastante bien aceptados en nuestro entorno y nos gustaría expandirnos más. Queremos tocar allí donde sea posible y que nos ayude a darnos a conocer.')
    portfolio2.artisticGender.add(artistic_gender4)
    portfolio2.zone.add(zone2)
    portfolio2.save()

    portfolio2_module1 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio2,
                                                        link='https://www.facebook.com/fromthenoise/')
    portfolio2_module1.save()

    portfolio2_module2 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio2,
                                                        link='https://www.facebook.com/batraciosvq/')
    portfolio2_module2.save()

    portfolio2_module3 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2,
                                                        link='https://www.youtube.com/watch?v=CEaJ-COP9Rs')
    portfolio2_module3.save()

    portfolio2_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio2,
                                                        link='https://www.youtube.com/watch?v=g43nbmB1cD8')
    portfolio2_module4.save()

    # ----

    portfolio3 = Portfolio.objects.create(artisticName='Los saraos',
                                          banner='https://c.pxhere.com/photos/9e/08/musicians_concert_flamenco_scene_music_art_scenario-1329878.jpg!d',
                                          biography='Considerados una de las principales figuras del flamenco actual, se le atribuye la responsabilidad de la reforma que llevó este arte a la escena musical internacional gracias a la inclusión de nuevos ritmos desde el jazz, la bossa nova y la música clásica. De este modo destacan sus colaboraciones con artistas internacionales como Carlos Santana, Al Di Meola o John McLaughlin, pero también con otras figuras del flamenco como Camarón de la Isla o Tomatito, con quienes modernizó el concepto de flamenco clásico.')
    portfolio3.artisticGender.add(artistic_gender5)
    portfolio3.zone.add(zone2)
    portfolio3.save()

    portfolio3_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio3,
                                                        description='Grupo Flamenco Saraos - 1',
                                                        link='https://www.youtube.com/watch?v=V599AxrB7P4')
    portfolio3_module4.save()

    portfolio3_module5 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio3,
                                                        description='Grupo Flamenco Saraos - 2',
                                                        link='https://www.youtube.com/watch?v=PZA5WVWzJd0')
    portfolio3_module5.save()

    # ----

    portfolio4 = Portfolio.objects.create(artisticName='Ana DJ',
                                          banner='https://c.pxhere.com/photos/52/a5/mixer_sound_board_sound_studio_broadcasting_radio_djs_music-1371930.jpg!d',
                                          biography='She may have been ‘born to be a DJ’, but sheer hard work and dedication are what’s brought ANNA success. In São Paulo, the traffic jams can stretch over a hundred miles on a bad day. Trapped under scorching sun or torrential rain, the air chewy and warm regardless, cars trudge along its roads and raised highways. Trees and shrubbery bring colour to the worn-out streets, sand-coloured and mirrored tower blocks looming large over the city. Beneath a concrete underpass in the north of the city, ANNA, aka DJ Ana Miranda, is making an emphatic return to the city that shaped her.')
    portfolio4.zone.add(zone4)
    portfolio4.artisticGender.add(artistic_gender2)
    portfolio4.save()

    portfolio4_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio4,
                                                        description='ANNA techno set at CRSSD Fest | Spring 2018',
                                                        link='https://www.youtube.com/watch?v=Up67slBkyRs')
    portfolio4_module1.save()

    portfolio4_module2 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio4,
                                                        description='ANNA Live from DJ Mag HQ',
                                                        link='https://www.youtube.com/watch?v=SCAHe6T-gK4')
    portfolio4_module2.save()

    # ----

    portfolio5 = Portfolio.objects.create(artisticName='Pasando olimpicamente',
                                          banner='https://live.staticflickr.com/2307/32502135310_db786fc360_k.jpg',
                                          biography='En 1989 monta la chirigota Los sanmolontropos con una música y una letra muy extraña que llama la atención hasta el punto que entran en la Final, de manera inesperada, sorprendiendo a propios y extraños. Siguiendo con esa línea de locura y surrealismo, al año siguiente saca la chirigota Carnaval 2036 Piconeros Galácticos. Se pregunta si pueden salir los 18 amigos en el Falla y decide hacer dos chirigotas. Le supuso un grandísimo esfuerzo y crea Ballet zum zum malacatum y El que la lleva la entiende (Los borrachos), en las que lleva la misma línea de surrealismo, pero pide por favor que fuera una chirigota interpretada porque le gusta mucho hacerse el borracho.')
    portfolio5.artisticGender.add(artistic_gender8)
    portfolio5.zone.add(zone4)
    portfolio5.save()

    portfolio5_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio5,
                                                        description='ANNA Live from DJ Mag HQ',
                                                        link='https://www.youtube.com/watch?v=W-8oEgRg5e8')
    portfolio5_module1.save()

    # ----

    portfolio6 = Portfolio.objects.create(artisticName='Una chirigota sin clase',
                                          banner='https://live.staticflickr.com/2307/32502135310_db786fc360_k.jpg',
                                          biography='En 1989 monta la chirigota Los sanmolontropos con una música y una letra muy extraña que llama la atención hasta el punto que entran en la Final, de manera inesperada, sorprendiendo a propios y extraños. Siguiendo con esa línea de locura y surrealismo, al año siguiente saca la chirigota Carnaval 2036 Piconeros Galácticos. Se pregunta si pueden salir los 18 amigos en el Falla y decide hacer dos chirigotas. Le supuso un grandísimo esfuerzo y crea Ballet zum zum malacatum y El que la lleva la entiende (Los borrachos), en las que lleva la misma línea de surrealismo, pero pide por favor que fuera una chirigota interpretada porque le gusta mucho hacerse el borracho.')
    portfolio6.artisticGender.add(artistic_gender8)
    portfolio6.zone.add(zone2)
    portfolio6.save()

    portfolio6_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio6,
                                                        description='Una chirigota sin clase - Preliminares',
                                                        link='https://www.youtube.com/watch?v=zm6JyvxOcd8')
    portfolio6_module1.save()

    portfolio6_module2 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio6,
                                                        description='Actuación en el Falla 2019 - 1',
                                                        link='https://www.codigocarnaval.com/wp-content/uploads/2018/12/Chirigota-Una-chirigota-sin-clase.jpg')
    portfolio6_module2.save()

    portfolio6_module3 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio6,
                                                        description='Actuación en el Falla 2019 - 2',
                                                        link='https://carnaval.lavozdigital.es/wp-content/uploads/2019/01/chirigota-sin-clase.jpg')
    portfolio6_module3.save()

    # ----

    portfolio7 = Portfolio.objects.create(artisticName='Batracio',
                                          banner='https://yt3.ggpht.com/IER5btMSGSaLEXOs8QTppGpgNCAs_yboMZCiPfLazmHoIPgSYuHqoIsJ61gEo-l-xQZOjNiRpg=w2560-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no',
                                          biography='Batracio nace en 2015, fruto de una reunión entre viejos amigos, Febes (voz) y José Alberto (guitarra) cansados de hacer en anteriores formaciones ḿúsica más genérica. De ahí no sólo nació una banda, sino que surgieron dos de sus temas más emblemáticos. La Charca y Pulgadas. Esto motivó a seguir adelante y continuar con un proyecto al que luego se sumarían Juan Bidegain (bajo), José Manuel Rodríguez “Negro” (teclado) y Javier Galliza (batería). Tras añadirse Domingo Muñoz (trombón) a la formación, sucedió el increíble debut en una mítica sala FunClub totalmente abarrotada. A partir de ese momento, las composiciones giraron hacia el Ska-funk característico de la banda. En 2016 la banda volvía al estudio para darle vida a Famelia y Souciedad.')
    portfolio7.artisticGender.add(artistic_gender3)
    portfolio7.artisticGender.add(artistic_gender4)
    portfolio7.zone.add(zone2)
    portfolio7.save()

    portfolio7_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio7, description='Group photo',
                                                        link='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/22089933_1594772467232483_3080874756432701823_n.jpg?_nc_cat=106&_nc_ht=scontent-mad1-1.xx&oh=def5d818429407165ba36763b4d352d6&oe=5D41A03B')
    portfolio7_module1.save()

    portfolio7_module2 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio7,
                                                        description='Canal de Facebook',
                                                        link='https://www.facebook.com/batraciosvq/')
    portfolio7_module2.save()

    portfolio7_module3 = PortfolioModule.objects.create(type='SOCIAL', portfolio=portfolio7,
                                                        description='Canal de Twitter',
                                                        link='https://twitter.com/batraciosvq')
    portfolio7_module3.save()

    portfolio7_module4 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                        description='No vuelvas ft Chusta (La Selva Sur)',
                                                        link='https://www.youtube.com/watch?v=g43nbmB1cD8')
    portfolio7_module4.save()

    portfolio7_module5 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7, description='Bona Fortuna',
                                                        link='https://www.youtube.com/watch?v=GB9AG5hDx4E')
    portfolio7_module5.save()

    portfolio7_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7, description='Souciedad',
                                                        link='https://www.youtube.com/watch?v=g7zqDQhxzzc')
    portfolio7_module6.save()

    portfolio7_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7, description='La Charca',
                                                        link='https://www.youtube.com/watch?v=WuLcH_W6iPg')
    portfolio7_module7.save()

    portfolio7_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                        description='Yo No Tonto Tanto',
                                                        link='https://www.youtube.com/watch?v=MC0nvRgKR30')
    portfolio7_module8.save()

    portfolio7_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                        description='Directo en Espartinas (La Raíz + Batracio + Sonido Vegetal)',
                                                        link='https://www.youtube.com/watch?v=GdQQUYCfSGw')
    portfolio7_module9.save()

    portfolio7_module10 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio7,
                                                         description='Moskojonera',
                                                         link='https://www.youtube.com/watch?v=9i2rM6dd5yA')
    portfolio7_module10.save()

    # ----

    portfolio8 = Portfolio.objects.create(artisticName='Medictum',
                                          banner='https://yt3.ggpht.com/IHxxu82dBWN8emRrLgn81-pjIdB6Q1qHW575Gmyk6zoAGxHEIHgXEwpZSaKLFH1KI_WlaEzX=w2560-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no',
                                          biography='MedictuM es una banda que surge en 2012 de la mano de los hermanos Antonio y Manuel Medina en su pueblo natal, Morón de la Frontera. Tras el paso de ambos por grupos locales, deciden crear su propio proyecto con toques de thrash metal, heavy metal clásico, pinceladas de hard rock y otros estilos.')
    portfolio8.artisticGender.add(artistic_gender3)
    portfolio8.artisticGender.add(artistic_gender4)
    portfolio8.zone.add(zone2)
    portfolio8.save()

    portfolio8_module1 = PortfolioModule.objects.create(type='PHOTO', portfolio=portfolio8, description='New disc!!!',
                                                        link='http://medictum.es/wp-content/uploads/2016/09/portadaweb.jpg')
    portfolio8_module1.save()

    portfolio8_module2 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8,
                                                        description='Antonio Medina',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-1.jpg')
    portfolio8_module2.save()

    portfolio8_module3 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8,
                                                        description='Manuel Medina',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-2.jpg')
    portfolio8_module3.save()

    portfolio8_module4 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8,
                                                        description='Rafael Córdoba',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-3.jpg')
    portfolio8_module4.save()

    portfolio8_module5 = PortfolioModule.objects.create(type='MEMBER', portfolio=portfolio8, description='Pablo Pérez',
                                                        link='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-4.jpg')
    portfolio8_module5.save()

    portfolio8_module6 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - El país de las pesadillas',
                                                        link='https://www.youtube.com/watch?v=EdUFDOM4lrU')
    portfolio8_module6.save()

    portfolio8_module7 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - Sala Palo Palo',
                                                        link='https://www.youtube.com/watch?v=bgqfkpxH5h0')
    portfolio8_module7.save()

    portfolio8_module8 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - Última oportunidad',
                                                        link='https://www.youtube.com/watch?v=fYzhR6g9J-4')
    portfolio8_module8.save()

    portfolio8_module9 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio8,
                                                        description='Medictum - Última oportunidad',
                                                        link='https://www.youtube.com/watch?v=9wSTyCbDicE')
    portfolio8_module9.save()

    # ----

    portfolio9 = Portfolio.objects.create(artisticName='Waterdogs',
                                          banner='https://cdn.pixabay.com/photo/2016/02/15/12/54/banner-1201119_1280.jpg',
                                          biography='It all began in 1997 when Martin Ekelund met Patrik Berglin and started to discuss music. They soon found out that they share the same taste in music. And what was more obvious then to start the best rockband in the world? Excactly…nothing! They found the drummer P-O Borg and started to write songs and rehearse. After a while P-O dropped the band and Martin and Patrik stood without a drummer. One warm and shiny day when the sky was blue and the world, for once, was a friendly and peacefull place, Martin came up with the brilliant idea of asking an old childhood friend to join the band. Hard hitting Daniel Persson united their forces and Waterdog was a fact.')
    portfolio9.artisticGender.add(artistic_gender3)
    portfolio9.artisticGender.add(artistic_gender4)
    portfolio9.zone.add(zone4)
    portfolio9.save()

    portfolio9_module1 = PortfolioModule.objects.create(type='VIDEO', portfolio=portfolio9,
                                                        description='Van Hallen - Dirty Water dog',
                                                        link='https://www.youtube.com/watch?v=30joGa9FhDw')
    portfolio9_module1.save()

    # Calendar

    availableDays1 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                      '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19']

    calendar1 = Calendar.objects.create(days=availableDays1, portfolio=portfolio1)
    calendar1.save()

    availableDays2 = ['2019-07-05', '2019-07-06', '2019-07-07', '2019-07-08', '2019-07-09', '2019-07-10',
                      '2019-07-11', '2019-08-15', '2019-08-16', '2019-10-13']

    calendar2 = Calendar.objects.create(days=availableDays2, portfolio=portfolio2)
    calendar2.save()

    availableDays3 = ['2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26',
                      '2019-07-27', '2019-07-28', '2019-08-16', '2019-08-17', '2019-08-18', '2019-08-19',
                      '2019-09-01', '2019-09-02', '2019-09-03', '2019-09-04', '2019-09-05', '2019-09-06',
                      '2019-09-07', '2019-09-08', '2019-09-09', '2019-09-10', '2019-09-11', '2019-09-12',
                      '2019-11-13', '2019-09-14', '2019-09-15', '2019-09-16', '2019-09-17', '2019-09-18',
                      '2019-12-21', '2019-12-23', '2019-12-24', '2019-12-25', '2019-12-26', '2019-12-27']

    calendar3 = Calendar.objects.create(days=availableDays3, portfolio=portfolio3)
    calendar3.save()

    availableDays4 = ['2019-05-21', '2019-05-22', '2019-05-23', '2019-05-24', '2019-05-25', '2019-05-26',
                      '2019-05-27', '2019-05-28', '2019-05-29', '2019-05-30', '2019-05-31',
                      '2019-06-01', '2019-06-02', '2019-06-03', '2019-06-04', '2019-06-05', '2019-06-06',
                      '2019-07-07', '2019-07-08', '2019-07-09', '2019-07-10', '2019-07-11', '2019-07-12',
                      '2019-08-01', '2019-08-02', '2019-08-03', '2019-08-04', '2019-08-05', '2019-08-06',
                      '2019-11-21', '2019-11-22', '2019-11-23', '2019-11-24', '2019-11-25', '2019-11-26']

    calendar4 = Calendar.objects.create(days=availableDays4, portfolio=portfolio4)
    calendar4.save()

    availableDays5 = ['2019-06-01', '2019-06-02', '2019-06-03', '2019-06-04', '2019-06-05', '2019-06-06',
                      '2019-07-04', '2019-07-05', '2019-07-06', '2019-07-07', '2019-07-08',
                      '2019-08-11', '2019-08-12', '2019-08-13', '2019-08-14', '2019-08-15', '2019-08-16',
                      '2019-08-17', '2019-08-18', '2019-08-19', '2019-08-20', '2019-08-21', '2019-08-22',
                      '2019-09-23', '2019-09-24', '2019-09-25', '2019-09-26', '2019-09-27', '2019-09-28',
                      '2019-11-01', '2019-11-02', '2019-11-03', '2019-11-04', '2019-11-05', '2019-11-06']

    calendar5 = Calendar.objects.create(days=availableDays5, portfolio=portfolio5)
    calendar5.save()

    availableDays6 = ['2019-04-06', '2019-04-07', '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11',
                      '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16', '2019-04-17',
                      '2019-05-03', '2019-05-04', '2019-05-05', '2019-05-06', '2019-05-07', '2019-05-08',
                      '2019-05-09', '2019-05-10', '2019-05-11', '2019-05-12', '2019-05-13', '2019-05-14',
                      '2019-06-17', '2019-06-18', '2019-06-19', '2019-06-20', '2019-06-21', '2019-06-22',
                      '2019-08-04', '2019-08-04', '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08']

    calendar6 = Calendar.objects.create(days=availableDays6, portfolio=portfolio6)
    calendar6.save()

    availableDays7 = ['2019-07-24', '2019-07-25', '2019-07-26', '2019-07-27', '2019-07-28', '2019-07-29',
                      '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08', '2019-08-09', '2019-08-10',
                      '2019-09-14', '2019-09-15', '2019-09-06', '2019-09-07', '2019-09-08', '2019-09-09',
                      '2019-11-15', '2019-11-16', '2019-11-17', '2019-11-18', '2019-11-19', '2019-11-20',
                      '2019-12-17', '2019-12-18', '2019-12-19', '2019-12-20', '2019-12-21', '2019-12-22',
                      '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09']

    calendar7 = Calendar.objects.create(days=availableDays7, portfolio=portfolio7)
    calendar7.save()

    availableDays8 = ['2019-04-06', '2019-04-07', '2019-04-08', '2019-04-09', '2019-04-10', '2019-04-11',
                      '2019-04-12', '2019-04-13', '2019-04-14', '2019-04-15', '2019-04-16', '2019-04-17',
                      '2019-05-03', '2019-05-04', '2019-05-05', '2019-05-06', '2019-05-07', '2019-05-08',
                      '2019-05-09', '2019-05-10', '2019-05-11', '2019-05-12', '2019-05-13', '2019-05-14',
                      '2019-06-17', '2019-06-18', '2019-06-19', '2019-06-20', '2019-06-21', '2019-06-22',
                      '2019-08-04', '2019-08-04', '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08',
                      '2020-01-04', '2020-01-05', '2020-01-06', '2020-01-07', '2020-01-08', '2020-01-09']

    calendar8 = Calendar.objects.create(days=availableDays8, portfolio=portfolio8)
    calendar8.save()

    # Users...

    # ,,,musician

    user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'),
                                        first_name='Carlos', last_name='Campos Cuesta',
                                        email='Joseph.jmlc@gmail.com')  # 'infoaudiowar@gmail.com'
    user1_artist1.save()
    user2_artist2 = User.objects.create(username='artist2', password=make_password('artist2artist2'),
                                        first_name='José Antonio', last_name='Granero Guzmán',
                                        email='Joseph.jmlc@gmail.com')  # josegraneroguzman@gmail.com
    user2_artist2.save()
    user3_artist3 = User.objects.create(username='artist3', password=make_password('artist3artist3'),
                                        first_name='Francisco', last_name='Martín',
                                        email='Joseph.jmlc@gmail.com')  # saralcum@gmail.com
    user3_artist3.save()
    user4_artist4 = User.objects.create(username='artist4', password=make_password('artist4artist4'), first_name='Ana',
                                        last_name='Mellado González',
                                        email='Joseph.jmlc@gmail.com')  # mellizalez@hotmail.com
    user4_artist4.save()
    user5_artist5 = User.objects.create(username='artist5', password=make_password('artist5artist5'),
                                        first_name='Alejandro', last_name='Arteaga Ramírez',
                                        email='Joseph.jmlc@gmail.com')  # alejandroarteagaramirez@gmail.com
    user5_artist5.save()
    user6_artist6 = User.objects.create(username='artist6', password=make_password('artist6artist6'),
                                        first_name='Pablo', last_name='Delgado Flores',
                                        email='Joseph.jmlc@gmail.com')  # pabloj.df@gmail.com
    user6_artist6.save()
    user7_artist7 = User.objects.create(username='artist7', password=make_password('artist7artist7'),
                                        first_name='Domingo', last_name='Muñoz Daza',
                                        email='Joseph.jmlc@gmail.com')  # dmunnoz96@gmail.com
    user7_artist7.save()
    user8_artist8 = User.objects.create(username='artist8', password=make_password('artist8artist8'),
                                        first_name='Rafael', last_name='Córdoba',
                                        email='Joseph.jmlc@gmail.com')  # contacto@medictum.es
    user8_artist8.save()
    user9_artist9 = User.objects.create(username='artist9', password=make_password('artist9artist9'),
                                        first_name='José Luis', last_name='Salvador Lauret',
                                        email='Joseph.jmlc@gmail.com')  # joseluis.salvador@gmail.com
    user9_artist9.save()

    # ...customers

    user10_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'),
                                           first_name='Rafael', last_name='Esquivias Ramírez',
                                           email='Joseph.jmlc@gmail.com')  # resquiviasramirez@gmail.com
    user10_customer1.save()
    user11_customer2 = User.objects.create(username='customer2', password=make_password('customer2customer2'),
                                           first_name='Jorge', last_name='Jimenez',
                                           email='Joseph.jmlc@gmail.com')  # jorjicorral@gmail.com
    user11_customer2.save()
    user12_customer3 = User.objects.create(username='customer3', password=make_password('customer3customer3'),
                                           first_name='Juan Manuel', last_name='Fernández',
                                           email='Joseph.jmlc@gmail.com')  # surlive@imgempresas.com
    user12_customer3.save()
    user13_customer4 = User.objects.create(username='customer4', password=make_password('customer4customer4'),
                                           first_name='Miguel', last_name='Romero Gutierrez',
                                           email='Joseph.jmlc@gmail.com')  # La posada Sevilla
    user13_customer4.save()

    # ...admins

    user14_admin = User.objects.create(username='admin', password=make_password('admin'), is_staff=True,
                                       is_superuser=True)
    user14_admin.save()

    # Artists

    artist1 = Artist.objects.create(user=user1_artist1, rating=4.5, portfolio=portfolio1, phone='600304999',
                                    photo='https://upload.wikimedia.org/wikipedia/commons/e/e7/Robin_Clark_%28DJ%29_Live_at_Techno4ever_net_Bday_Rave.jpg',
                                    iban='ES6621000418401234567891', paypalAccount='bwer0192@gmail.com')
    artist1.save()
    artist2 = Artist.objects.create(user=user2_artist2, rating=4.9, portfolio=portfolio2, phone='695099812',
                                    photo='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/20953179_10155798140312625_5517808811547907373_n.jpg?_nc_cat=108&_nc_ht=scontent-mad1-1.xx&oh=78561ec93ba4604a3c5a570cbe101b40&oe=5D4D1ED1',
                                    iban='ES1720852066623456789011')
    artist2.save()
    artist3 = Artist.objects.create(user=user3_artist3, rating=4.0, portfolio=portfolio3, phone='695990241',
                                    photo='https://cdn.pixabay.com/photo/2016/02/19/11/36/microphone-1209816_1280.jpg',
                                    iban='ES6000491500051234567892')
    artist3.save()
    artist4 = Artist.objects.create(user=user4_artist4, rating=3.5, portfolio=portfolio4, phone='610750391',
                                    photo='https://www.billboard.com/files/media/Dani-Deahl-press-photo-2016-billboard-1000.jpg',
                                    iban='ES9420805801101234567891')
    artist4.save()
    artist5 = Artist.objects.create(user=user5_artist5, rating=4.5, portfolio=portfolio5, phone='675181175',
                                    photo='https://carnaval.lavozdigital.es/wp-content/uploads/2019/01/chirigota-pasando-olimpicamente-recortada.jpg',
                                    iban='ES9000246912501234567891')
    artist5.save()
    artist6 = Artist.objects.create(user=user6_artist6, rating=4.0, portfolio=portfolio6, phone='673049277',
                                    photo='https://carnaval.lavozdigital.es/wp-content/uploads/2019/01/chirigota-sin-clase.jpg',
                                    iban='ES7100302053091234567895')
    artist6.save()
    artist7 = Artist.objects.create(user=user7_artist7, rating=4.75, portfolio=portfolio7, phone='664196105',
                                    photo='https://scontent-mad1-1.xx.fbcdn.net/v/t1.0-9/50732294_2114221071976992_2173326934371467264_o.jpg?_nc_cat=100&_nc_ht=scontent-mad1-1.xx&oh=dacf068903a3703434b52cfade783470&oe=5D09C938',
                                    iban='ES1000492352082414205416')
    artist7.save()
    artist8 = Artist.objects.create(user=user8_artist8, rating=4.66666666, portfolio=portfolio8, phone='664596466',
                                    photo='http://medictum.es/wp-content/uploads/2017/03/p2-team-image-3.jpg',
                                    iban='ES1720852066623456789011')
    artist8.save()
    artist9 = Artist.objects.create(user=user9_artist9, rating=3.75, portfolio=portfolio9, phone='679739257',
                                    photo='https://media.licdn.com/dms/image/C4E03AQFAONXIX44h6w/profile-displayphoto-shrink_800_800/0?e=1559174400&v=beta&t=eEhhR1sr9-p1fr1tREXmlXV6WAzPvNlFDHhlV8SNwRY',
                                    iban='ES9420805801101234567891')
    artist9.save()

    # Customers with credit card

    customer1 = Customer.objects.create(user=user10_customer1, phone='639154189', holder='Rafael Esquivias Ramírez',
                                        expirationDate='2020-10-01', number='4651001401188232')
    customer1.save()
    customer2 = Customer.objects.create(user=user11_customer2, phone='664656659', holder='Jorge Jiménez del Corral',
                                        expirationDate='2027-03-01', number='4934521448108546')
    customer2.save()
    customer3 = Customer.objects.create(user=user12_customer3, phone='678415820', holder='Juan Manuel Fernández',
                                        expirationDate='2025-10-01', number='4656508395720981')
    customer3.save()
    customer4 = Customer.objects.create(user=user13_customer4, phone='627322721', holder='Miguel Romero Gutierrez',
                                        expirationDate='2027-03-01', number='4826704855401486')
    customer4.save()

    # Event location

    event_location1 = EventLocation.objects.create(name='Event 1 - Festival Rockupo',
                                                   address='Universidad Pablo de Olavide', equipment='No', zone=zone2,
                                                   customer=customer1)
    event_location1.save()
    event_location2 = EventLocation.objects.create(name='Event 2 - La Posada Sevilla',
                                                   address='C/Astronomía, 42, 41015',
                                                   equipment='Yes, we have al equipment necesary, we have concerts every week, we have all you need for this job.',
                                                   zone=zone2,
                                                   customer=customer2)
    event_location2.save()
    event_location3 = EventLocation.objects.create(name='Event 3 - Rosalia en vivo', address='C/Sol, 45, 41652',
                                                   equipment='No', zone=zone2, customer=customer3)
    event_location3.save()
    event_location4 = EventLocation.objects.create(name='Event 4 - Charlie XCX', address='C/Amalgama, 2, 41609',
                                                   equipment='Yes, we have a stage of 30 square meters, a system of loudspeakers distributed by the local, with a total of 16 loudspeakers and a complete system of LED lights that can be adjusted to the intensity and color desired.',
                                                   zone=zone4, customer=customer4)
    event_location4.save()

    # Payment packages with Payment types

    performance1_paymentPackage1 = Performance.objects.create(info='Performance Payment Type from Carlos DJ',
                                                              hours=1.5, price=50)
    performance1_paymentPackage1.save()

    paymentPackage1_performance1 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Carlos DJ',
        portfolio=portfolio1,
        performance=performance1_paymentPackage1)
    paymentPackage1_performance1.save()

    fare1_paymentPackage2 = Fare.objects.create(priceHour=45)
    fare1_paymentPackage2.save()

    paymentPackage2_fare1 = PaymentPackage.objects.create(description='Fare Payment Package Type from Carlos DJ',
                                                          portfolio=portfolio1,
                                                          fare=fare1_paymentPackage2)
    paymentPackage2_fare1.save()

    custom1_paymentPackage3 = Custom.objects.create(minimumPrice=60)
    custom1_paymentPackage3.save()

    paymentPackage3_custom1 = PaymentPackage.objects.create(description='Custom Payment Package Type from Carlos DJ',
                                                            portfolio=portfolio1,
                                                            custom=custom1_paymentPackage3)
    paymentPackage3_custom1.save()

    # ----

    performance2_paymentPackage4 = Performance.objects.create(info='Performance Payment Type from From the noise',
                                                              hours=1.5, price=50)
    performance2_paymentPackage4.save()

    paymentPackage4_performance2 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from From the noise',
        portfolio=portfolio2,
        performance=performance2_paymentPackage4)
    paymentPackage4_performance2.save()

    fare2_paymentPackage5 = Fare.objects.create(priceHour=45)
    fare2_paymentPackage5.save()

    paymentPackage5_fare2 = PaymentPackage.objects.create(description='Fare Payment Package Type from From the noise',
                                                          portfolio=portfolio2,
                                                          fare=fare2_paymentPackage5)
    paymentPackage5_fare2.save()

    custom2_paymentPackage6 = Custom.objects.create(minimumPrice=60)
    custom2_paymentPackage6.save()

    paymentPackage6_custom2 = PaymentPackage.objects.create(
        description='Custom Payment Package Type from From the noise',
        portfolio=portfolio2,
        custom=custom2_paymentPackage6)
    paymentPackage6_custom2.save()

    # ----

    performance3_paymentPackage7 = Performance.objects.create(info='Performance Payment Type from Los saraos',
                                                              hours=1.5, price=50)
    performance3_paymentPackage7.save()

    paymentPackage7_performance3 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Los saraos',
        portfolio=portfolio3,
        performance=performance3_paymentPackage7)
    paymentPackage7_performance3.save()

    fare3_paymentPackage8 = Fare.objects.create(priceHour=45)
    fare3_paymentPackage8.save()

    paymentPackage8_fare3 = PaymentPackage.objects.create(description='Fare Payment Package Type from Los saraos',
                                                          portfolio=portfolio3,
                                                          fare=fare3_paymentPackage8)
    paymentPackage8_fare3.save()

    custom3_paymentPackage9 = Custom.objects.create(minimumPrice=60)
    custom3_paymentPackage9.save()

    paymentPackage9_custom3 = PaymentPackage.objects.create(description='Custom Payment Package Type from Los saraos',
                                                            portfolio=portfolio3,
                                                            custom=custom3_paymentPackage9)
    paymentPackage9_custom3.save()

    # ----

    performance4_paymentPackage10 = Performance.objects.create(info='Performance Payment Type from Ana DJ',
                                                               hours=1.5, price=50)
    performance4_paymentPackage10.save()

    paymentPackage10_performance4 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Ana DJ',
        portfolio=portfolio4,
        performance=performance4_paymentPackage10)
    paymentPackage10_performance4.save()

    fare4_paymentPackage11 = Fare.objects.create(priceHour=45)
    fare4_paymentPackage11.save()

    paymentPackage11_fare3 = PaymentPackage.objects.create(description='Fare Payment Package Type from Ana DJ',
                                                           portfolio=portfolio4,
                                                           fare=fare4_paymentPackage11)
    paymentPackage11_fare3.save()

    custom4_paymentPackage12 = Custom.objects.create(minimumPrice=60)
    custom4_paymentPackage12.save()

    paymentPackage12_custom4 = PaymentPackage.objects.create(description='Custom Payment Package Type from Ana DJ',
                                                             portfolio=portfolio4,
                                                             custom=custom4_paymentPackage12)
    paymentPackage12_custom4.save()

    # ----

    performance5_paymentPackage13 = Performance.objects.create(
        info='Performance Payment Type from Pasando olimpicamente',
        hours=1.5, price=50)
    performance5_paymentPackage13.save()

    paymentPackage13_performance5 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Pasando olimpicamente',
        portfolio=portfolio5,
        performance=performance5_paymentPackage13)
    paymentPackage13_performance5.save()

    fare5_paymentPackage14 = Fare.objects.create(priceHour=45)
    fare5_paymentPackage14.save()

    paymentPackage14_fare5 = PaymentPackage.objects.create(
        description='Fare Payment Package Type from Pasando olimpicamente',
        portfolio=portfolio5,
        fare=fare5_paymentPackage14)
    paymentPackage14_fare5.save()

    custom5_paymentPackage15 = Custom.objects.create(minimumPrice=60)
    custom5_paymentPackage15.save()

    paymentPackage15_custom5 = PaymentPackage.objects.create(
        description='Custom Payment Package Type from Pasando olimpicamente',
        portfolio=portfolio5,
        custom=custom5_paymentPackage15)
    paymentPackage15_custom5.save()

    # ----

    performance6_paymentPackage16 = Performance.objects.create(
        info='Performance Payment Type from Una chirigota con clase',
        hours=1.5, price=50)
    performance6_paymentPackage16.save()

    paymentPackage16_performance6 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Una chirigota con clase',
        portfolio=portfolio6,
        performance=performance6_paymentPackage16)
    paymentPackage16_performance6.save()

    fare6_paymentPackage17 = Fare.objects.create(priceHour=45)
    fare6_paymentPackage17.save()

    paymentPackage17_fare6 = PaymentPackage.objects.create(
        description='Fare Payment Package Type from Una chirigota con clase',
        portfolio=portfolio6,
        fare=fare6_paymentPackage17)
    paymentPackage17_fare6.save()

    custom6_paymentPackage18 = Custom.objects.create(minimumPrice=60)
    custom6_paymentPackage18.save()

    paymentPackage18_custom6 = PaymentPackage.objects.create(
        description='Custom Payment Package Type from Una chirigota con clase',
        portfolio=portfolio6,
        custom=custom6_paymentPackage18)
    paymentPackage18_custom6.save()

    # ----

    performance7_paymentPackage19 = Performance.objects.create(info='Performance Payment Type from Batracio',
                                                               hours=1.5, price=50)
    performance7_paymentPackage19.save()

    paymentPackage19_performance7 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Batracio',
        portfolio=portfolio7,
        performance=performance7_paymentPackage19)
    paymentPackage19_performance7.save()

    fare7_paymentPackage20 = Fare.objects.create(priceHour=45)
    fare7_paymentPackage20.save()

    paymentPackage20_fare7 = PaymentPackage.objects.create(description='Fare Payment Package Type from Batracio',
                                                           portfolio=portfolio7,
                                                           fare=fare7_paymentPackage20)
    paymentPackage20_fare7.save()

    custom7_paymentPackage21 = Custom.objects.create(minimumPrice=60)
    custom7_paymentPackage21.save()

    paymentPackage21_custom7 = PaymentPackage.objects.create(description='Custom Payment Package Type from Batracio',
                                                             portfolio=portfolio7,
                                                             custom=custom7_paymentPackage21)
    paymentPackage21_custom7.save()

    # ----

    performance8_paymentPackage22 = Performance.objects.create(info='Performance Payment Type from Medictum',
                                                               hours=1.5, price=50)
    performance8_paymentPackage22.save()

    paymentPackage22_performance8 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Medictum',
        portfolio=portfolio8,
        performance=performance8_paymentPackage22)
    paymentPackage22_performance8.save()

    fare8_paymentPackage23 = Fare.objects.create(priceHour=45)
    fare8_paymentPackage23.save()

    paymentPackage23_fare8 = PaymentPackage.objects.create(description='Fare Payment Package Type from Medictum',
                                                           portfolio=portfolio8,
                                                           fare=fare8_paymentPackage23)
    paymentPackage23_fare8.save()

    custom8_paymentPackage24 = Custom.objects.create(minimumPrice=60)
    custom8_paymentPackage24.save()

    paymentPackage24_custom8 = PaymentPackage.objects.create(description='Custom Payment Package Type from Medictum',
                                                             portfolio=portfolio8,
                                                             custom=custom8_paymentPackage24)
    paymentPackage24_custom8.save()

    # ----

    performance9_paymentPackage25 = Performance.objects.create(info='Performance Payment Type from Waterdogs',
                                                               hours=1.5, price=50)
    performance9_paymentPackage25.save()

    paymentPackage25_performance9 = PaymentPackage.objects.create(
        description='Performance Payment Package Type from Waterdogs',
        portfolio=portfolio9,
        performance=performance9_paymentPackage25)
    paymentPackage25_performance9.save()

    fare9_paymentPackage26 = Fare.objects.create(priceHour=45)
    fare9_paymentPackage26.save()

    paymentPackage26_fare9 = PaymentPackage.objects.create(description='Fare Payment Package Type from Waterdogs',
                                                           portfolio=portfolio9,
                                                           fare=fare9_paymentPackage26)
    paymentPackage26_fare9.save()

    custom9_paymentPackage27 = Custom.objects.create(minimumPrice=60)
    custom9_paymentPackage27.save()

    paymentPackage27_custom9 = PaymentPackage.objects.create(description='Custom Payment Package Type from Waterdogs',
                                                             portfolio=portfolio9,
                                                             custom=custom9_paymentPackage27)
    paymentPackage27_custom9.save()



    # Transactions
    transaction_offer1 = Transaction.objects.create(paypalArtist='bwer0192@gmail.com', amount="120")
    transaction_offer1.save()

    transaction_offer2 = Transaction.objects.create()
    transaction_offer2.save()

    transaction_offer3 = Transaction.objects.create()
    transaction_offer3.save()

    transaction_offer4 = Transaction.objects.create()
    transaction_offer4.save()

    transaction_offer5 = Transaction.objects.create()
    transaction_offer5.save()

    transaction_offer6 = Transaction.objects.create()
    transaction_offer6.save()

    transaction_offer7 = Transaction.objects.create()
    transaction_offer7.save()

    transaction_offer8 = Transaction.objects.create()
    transaction_offer8.save()

    transaction_offer9 = Transaction.objects.create()
    transaction_offer9.save()

    transaction_offer10 = Transaction.objects.create()
    transaction_offer10.save()

    transaction_offer11 = Transaction.objects.create()
    transaction_offer11.save()

    transaction_offer12 = Transaction.objects.create()
    transaction_offer12.save()

    transaction_offer13 = Transaction.objects.create()
    transaction_offer13.save()

    transaction_offer14 = Transaction.objects.create()
    transaction_offer14.save()

    transaction_offer15 = Transaction.objects.create()
    transaction_offer15.save()

    transaction_offer16 = Transaction.objects.create()
    transaction_offer16.save()

    transaction_offer17 = Transaction.objects.create()
    transaction_offer17.save()

    transaction_offer18 = Transaction.objects.create()
    transaction_offer18.save()

    transaction_offer19 = Transaction.objects.create()
    transaction_offer19.save()

    # Rating
    rating_offer2 = Rating.objects.create(score=5, comment="Lo ha hecho explendido")
    rating_offer3 = Rating.objects.create(score=4, comment="Lo ha hecho muy bien")

    # Offers

    offer1_performance1 = Offer.objects.create(description='Oferta 1 to Carlos DJ by performance', status='CONTRACT_MADE',
                                               date='2019-04-29 12:00:00', hours=2.5, price='120', currency='EUR',
                                               appliedVAT=7, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1, transaction=transaction_offer1,
                                               paymentCode=_service_generate_unique_payment_code())
    offer1_performance1.save()

    offer2_performance1 = Offer.objects.create(description='Oferta 2 to Carlos DJ by performance',
                                               status='PAYMENT_MADE',
                                               date='2019-07-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=7, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1, transaction=transaction_offer2,
                                               rating=rating_offer2)
    offer2_performance1.save()

    offer3_performance1 = Offer.objects.create(description='Oferta 3 to Carlos DJ by performance',
                                               status='PAYMENT_MADE',
                                               date='2019-08-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=7, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location1, transaction=transaction_offer3,
                                               rating=rating_offer3)
    offer3_performance1.save()

    offer4_performance1 = Offer.objects.create(description='Oferta 4 to Carlos DJ by performance',
                                               status='CANCELLED_ARTIST',
                                               date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=7, paymentPackage=paymentPackage1_performance1,
                                               eventLocation=event_location2, transaction=transaction_offer4)
    offer4_performance1.save()

    offer5_fare1 = Offer.objects.create(description='Oferta 5 to Carlos DJ by fare', status='PENDING',
                                        date='2019-10-25 12:00:00', hours=1.5, price='120', currency='EUR',
                                        appliedVAT=7, paymentPackage=paymentPackage2_fare1,
                                        eventLocation=event_location2, transaction=transaction_offer5)
    offer5_fare1.save()

    offer6_custom1 = Offer.objects.create(description='Oferta 6 to Carlos DJ by custom', status='CONTRACT_MADE',
                                          date='2019-8-25 12:00:00', hours=1.5, price='115', currency='EUR',
                                          appliedVAT=7, paymentCode=_service_generate_unique_payment_code(),
                                          paymentPackage=paymentPackage3_custom1,
                                          eventLocation=event_location1, transaction=transaction_offer6)
    offer6_custom1.save()

    offer7_custom1 = Offer.objects.create(description='Oferta 7 to Carlos DJ by custom', status='REJECTED',
                                          date='2019-10-25 19:00:00', hours=1.5, price='100', currency='EUR',
                                          appliedVAT=7, paymentPackage=paymentPackage3_custom1,
                                          eventLocation=event_location1, transaction=transaction_offer7)
    offer7_custom1.save()

    offer8_performance2 = Offer.objects.create(description='Oferta 8 to From the noise by performance',
                                               status='REJECTED',
                                               date='2019-10-25 15:00:00', hours=1.5, price='140', currency='EUR',
                                               appliedVAT=7, paymentPackage=paymentPackage4_performance2,
                                               eventLocation=event_location1, transaction=transaction_offer8)
    offer8_performance2.save()

    offer9_performance2 = Offer.objects.create(description='Oferta 9 to From the noise by performance',
                                               status='CONTRACT_MADE',
                                               date='2019-10-25 15:00:00', hours=1.5, price='140', currency='EUR',
                                               paymentCode=_service_generate_unique_payment_code(),
                                               appliedVAT=7, paymentPackage=paymentPackage4_performance2,
                                               eventLocation=event_location1, transaction=transaction_offer9)
    offer9_performance2.save()

    offer10_fare2 = Offer.objects.create(description='Oferta 10 to From the noise by fare', status='CANCELLED_ARTIST',
                                         date='2019-03-27 00:00:00', hours=1.5, price='140', currency='EUR',
                                         paymentCode=_service_generate_unique_payment_code(),
                                         appliedVAT=7, paymentPackage=paymentPackage5_fare2,
                                         eventLocation=event_location4, transaction=transaction_offer10)
    offer10_fare2.save()

    offer11_fare2 = Offer.objects.create(description='Oferta 11 to From the noise by fare', status='CONTRACT_MADE',
                                         date='2019-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                         paymentCode=_service_generate_unique_payment_code(),
                                         appliedVAT=7, paymentPackage=paymentPackage5_fare2,
                                         eventLocation=event_location4, transaction=transaction_offer11)
    offer11_fare2.save()

    offer12_custom2 = Offer.objects.create(description='Oferta 12 to From the noise by fare', status='CONTRACT_MADE',
                                           date='2019-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                           paymentCode=_service_generate_unique_payment_code(),
                                           appliedVAT=7, paymentPackage=paymentPackage5_fare2,
                                           eventLocation=event_location3, transaction=transaction_offer12)
    offer12_custom2.save()

    offer13_custom2 = Offer.objects.create(description='Oferta 13 to From the noise by fare',
                                           status='CANCELLED_CUSTOMER',
                                           date='2017-01-06 01:00:00', hours=1.5, price='140', currency='EUR',
                                           paymentCode=_service_generate_unique_payment_code(),
                                           appliedVAT=7, paymentPackage=paymentPackage5_fare2,
                                           eventLocation=event_location3, transaction=transaction_offer13)
    offer13_custom2.save()

    offer14_performance2 = Offer.objects.create(description='Oferta 14 to From the noise by performance',
                                                status='PENDING',
                                                date='2019-07-07 15:00:00', hours=2.5, price='115', currency='EUR',
                                                appliedVAT=7, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location1, transaction=transaction_offer14)

    offer14_performance2.save()

    offer19_performance2 = Offer.objects.create(description='Oferta 15 to From the noise by performance',
                                                status='PENDING',
                                                date='2019-07-11 15:00:00', hours=1.5, price='80', currency='EUR',
                                                appliedVAT=7, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location2, transaction=transaction_offer19)

    offer19_performance2.save()

    offer15_performance1 = Offer.objects.create(description='Oferta 16 to Carlos DJ by performance', status='PENDING',
                                                date='2019-07-11 15:00:00', hours=2.5, price='160', currency='EUR',
                                                appliedVAT=7, paymentPackage=paymentPackage1_performance1,
                                                eventLocation=event_location1, transaction=transaction_offer15)

    offer15_performance1.save()

    offer16_performance1 = Offer.objects.create(description='Oferta 17 to Carlos DJ by performance', status='PENDING',
                                                date='2019-07-14 08:00:00', hours=1.5, price='800', currency='EUR',
                                                appliedVAT=7, paymentPackage=paymentPackage1_performance1,
                                                eventLocation=event_location2, transaction=transaction_offer16)

    offer16_performance1.save()

    offer17_performance1 = Offer.objects.create(description='Oferta 18 to From the noise by performance',
                                                status='PAYMENT_MADE',
                                                date='2019-03-14 08:00:00', hours=3, price='1000', currency='EUR',
                                                appliedVAT=21, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location1, transaction=transaction_offer17,paymentCode=_service_generate_unique_payment_code())

    offer17_performance1.save()

    offer18_performance1 = Offer.objects.create(description='Oferta 19 to From the noise by performance',
                                                status='PAYMENT_MADE',
                                                date='2019-03-14 12:00:00', hours=3.1, price='1200', currency='EUR',
                                                appliedVAT=21, paymentPackage=paymentPackage4_performance2,
                                                eventLocation=event_location1, transaction=transaction_offer18,paymentCode=_service_generate_unique_payment_code())

    offer18_performance1.save()



os.system('python3 manage.py sqlflush | python3 manage.py dbshell')
save_data()
#index_all()
