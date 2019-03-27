import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()

from Grooving.models import ArtisticGender, Portfolio, Artist, Zone, PortfolioModule, Calendar, PaymentPackage, Performance, Fare, Custom, Offer, Customer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def delete_data():
     User.objects.all().delete()
     Artist.objects.all().delete()
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

     # Admin

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

     # Representante Alejandro Arteaga Ramírez

     portfolio5 = Portfolio.objects.create(artisticName='Pasando olimpicamente')
     portfolio5.artisticGender.add(artistic_gender8)
     portfolio5.zone.add(zone2)
     portfolio5.save()

     # Representante Pablo Delgado Flores Pablo

     portfolio6 = Portfolio.objects.create(artisticName='Una chirigota sin clase')
     portfolio6.artisticGender.add(artistic_gender8)
     portfolio6.zone.add(zone1)
     portfolio6.save()

     # Representante Domingo Muñoz Plaza

     portfolio7 = Portfolio.objects.create(artisticName='Batracio')
     portfolio7.artisticGender.add(artistic_gender3)
     portfolio7.artisticGender.add(artistic_gender4)
     portfolio7.zone.add(zone1)
     portfolio7.save()

     # Representante [PENDIENTE]

     portfolio8 = Portfolio.objects.create(artisticName='Medictum')
     portfolio8.artisticGender.add(artistic_gender3)
     portfolio8.artisticGender.add(artistic_gender4)
     portfolio8.zone.add(zone1)
     portfolio8.save()


     # Representante José Luis Salvador Lauret

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

     # Artist with user

     user1_artist1 = User.objects.create(username='artist1', password=make_password('artist1artist1'))
     user2_customer1 = User.objects.create(username='customer1', password=make_password('customer1customer1'))
     user1_admin = User.objects.create(username='admin', password=make_password('admin'), is_staff=True, is_superuser=True)
     artist1 = Artist.objects.create(user=user1_artist1, portfolio=portfolio1)
     customer1 = Customer.objects.create(user=user2_customer1)





     # Offers

     # offer1 = Offer.objects.create(description='Oferta 1', status='PENDING', date='', hours=2.5, price='',
                                   # currency='EUR', paymentCode='')
     # offer2 = Offer.objects.create()

     # Artists

     # artist1 = Artist.objects.create(photo=None, phone='634753516', iban='ES8320959158157673223562', paypalAccount=None,
     #                                portfolio=portfolio1)


delete_data()
save_data()

