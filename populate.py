import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Server.settings")
django.setup()

from Grooving.models import ArtisticGender, Portfolio, Artist


def delete_data():
     ArtisticGender.objects.all().delete()
     Portfolio.objects.all().delete()


def save_data():

     # Admin

     # ArtisticGenders

     artistic_gender1 = ArtisticGender(name='Music')
     artistic_gender1.save()

     artistic_gender2 = ArtisticGender(name='DJ', parentGender=artistic_gender1)
     artistic_gender2.save()

     artistic_gender3 = ArtisticGender(name='Pop', parentGender=artistic_gender1)
     artistic_gender3.save()

     artistic_gender4 = ArtisticGender(name='Rock', parentGender=artistic_gender1)
     artistic_gender4.save()

     artistic_gender5 = ArtisticGender(name='Flamenco', parentGender=artistic_gender1)
     artistic_gender5.save()

     artistic_gender6 = ArtisticGender(name='Magician')
     artistic_gender6.save()

     artistic_gender7 = ArtisticGender(name='Comedian')
     artistic_gender7.save()

     artistic_gender8 = ArtisticGender(name='Carnival')
     artistic_gender8.save()


     # Portfolios

     portfolio1 = Portfolio.objects.create(artisticName='Carlos DJ')
     portfolio1.artisticGender.add(artistic_gender2)
     portfolio1.save()

     portfolio2 = Portfolio.objects.create(artisticName='From the noise')
     portfolio2.artisticGender.add(artistic_gender4)
     portfolio2.save()

     portfolio3 = Portfolio.objects.create(artisticName='Los saraos')
     portfolio3.artisticGender.add(artistic_gender5)
     portfolio3.save()

     portfolio4 = Portfolio.objects.create(artisticName='Ana DJ')
     portfolio4.artisticGender.add(artistic_gender2)
     portfolio4.save()

     # Representante Alejandro Arteaga Ramírez

     portfolio5 = Portfolio.objects.create(artisticName='Pasando olimpicamente')
     portfolio5.artisticGender.add(artistic_gender8)
     portfolio5.save()

     # Representante Pablo Delgado Flores Pablo

     portfolio6 = Portfolio.objects.create(artisticName='Una chirigota sin clase')
     portfolio6.artisticGender.add(artistic_gender8)
     portfolio6.save()

     # Representante Domingo Muñoz Plaza

     portfolio7 = Portfolio.objects.create(artisticName='Batracio')
     portfolio7.artisticGender.add(artistic_gender3)
     portfolio7.artisticGender.add(artistic_gender4)
     portfolio7.save()

     # Representante [PENDIENTE]

     portfolio8 = Portfolio.objects.create(artisticName='Medictum')
     portfolio8.artisticGender.add(artistic_gender3)
     portfolio8.artisticGender.add(artistic_gender4)
     portfolio8.save()

     # Representante José Luis Salvador Lauret

     portfolio9 = Portfolio.objects.create(artisticName='Waterdogs')
     portfolio9.artisticGender.add(artistic_gender3)
     portfolio9.artisticGender.add(artistic_gender4)
     portfolio9.save()


     # Artists

     artist1 = Artist.objects.create(photo=None, phone='634753516', iban='ES8320959158157673223562', paypalAccount=None, portfolio=portfolio1)

     #

delete_data()
save_data()

