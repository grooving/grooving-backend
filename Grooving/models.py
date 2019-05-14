from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField, JSONField
from django.utils import timezone
import time
# Create your models here.

fotoType = (
    ('PROFILE', 'PROFILE'),
    ('BANNER', 'BANNER'),
    ('CAROUSEL', 'CAROUSEL'),
    )

def get_time_stamp():
    return int(round(time.time() * 1000))


class Upload(models.Model):
    file = models.FileField()
    type = models.CharField(choices=fotoType, max_length=50)
    userId = models.IntegerField()
    timeStamp = models.BigIntegerField(default=get_time_stamp)



class AbstractEntity(models.Model):
    creationMoment = models.DateTimeField(auto_now_add=True)
    lastModification = models.DateTimeField(auto_now=True)
    isHidden = models.BooleanField(default=False)

    class Meta:
        abstract = True


LanguageField = (
    ('es', 'es'),
    ('en', 'en'))


class Actor(AbstractEntity):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(choices=LanguageField, max_length=3, default="en")

    def __str__(self):
        return str(self.user.username)

    class Meta:
        abstract = True


class Admin(Actor):
    pass

    def __str__(self):
        return str(self.user.username)


class UserAbstract(Actor):
    photo = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    iban = models.CharField(max_length=34, blank=True, null=True)
    paypalAccount = models.EmailField(blank=True, null=True)

    class Meta:
        abstract = True


class ArtisticGender(AbstractEntity):
    name_en = models.CharField(max_length=140)
    name_es = models.CharField(max_length=140)
    parentGender = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name_en)


class Zone(AbstractEntity):
    name = models.CharField(max_length=140)
    parentZone = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Portfolio(AbstractEntity):
    banner = models.CharField(blank=True, null=True, max_length=500)
    biography = models.TextField(blank=True, null=True)
    artist = models.OneToOneField('Artist', related_name='portfolio', null=True, blank=True, on_delete=models.SET_NULL)
    artisticName = models.CharField(unique=True, blank=True, null=True, max_length=140)
    artisticGender = models.ManyToManyField(ArtisticGender, blank=True)
    zone = models.ManyToManyField(Zone, blank=True)

    def __str__(self):
        return str(self.artisticName)


class Calendar(AbstractEntity):
    days = ArrayField(models.CharField(max_length=10), null=True)
    portfolio = models.OneToOneField(Portfolio, on_delete=models.CASCADE)


class Artist(UserAbstract):
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0,
                                 validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))])


ModuleTypeField = (
    ('PHOTO', 'PHOTO'),
    ('VIDEO', 'VIDEO'),
    ('AUDIO', 'AUDIO'),
    ('TWITTER', 'TWITTER'),
    ('INSTAGRAM', 'INSTAGRAM'),
    ('MEMBER', 'MEMBER'))


class PortfolioModule(AbstractEntity):
    type = models.CharField(choices=ModuleTypeField, max_length=50)
    link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.type) + ' - ' + str(self.description)


class Performance(AbstractEntity):
    info = models.TextField()
    hours = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.5'))])
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('1.0'))])


class Fare(AbstractEntity):
    priceHour = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('2.0'))])


class Custom(AbstractEntity):
    minimumPrice = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('1.0'))])


class PaymentPackage(AbstractEntity):
    description = models.TextField(blank=True, null=True)
    currency = models.CharField(default='EUR', max_length=3)
    portfolio = models.ForeignKey(Portfolio, related_name='paymentPackages', on_delete=models.PROTECT)
    performance = models.OneToOneField(Performance, null=True, on_delete=models.SET_NULL)
    fare = models.OneToOneField(Fare, null=True, on_delete=models.SET_NULL)
    custom = models.OneToOneField(Custom, null=True, on_delete=models.SET_NULL)


class Customer(UserAbstract):
    holder = models.CharField(blank=True, null=True, max_length=255)
    expirationDate = models.DateField(blank=True, null=True)
    number = models.CharField(blank=True, null=True, max_length=16)


class EventLocation(AbstractEntity):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255)
    equipment = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    customer = models.ForeignKey(Customer, null=True, related_name="eventLocations", blank=True,
                                 on_delete=models.SET_NULL)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.name)


OfferStatusField = (
    ('PENDING', "PENDING"),
    ('NEGOTIATION', "NEGOTIATION"),
    ('CONTRACT_MADE', "CONTRACT_MADE"),
    ('WITHDRAWN', "WITHDRAWN"),
    ('REJECTED', "REJECTED"),
    ('CANCELLED_ARTIST', 'CANCELLED_ARTIST'),
    ('CANCELLED_CUSTOMER', 'CANCELLED_CUSTOMER'),
    ('PAYMENT_MADE', "PAYMENT_MADE"))


class Transaction(AbstractEntity):

    amount = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('0.3'))], null=True)
    braintree_id = models.CharField(blank=True, null=True, max_length=70)
    paypalArtist = models.EmailField(blank=True, null=True)


class Rating(AbstractEntity):
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)


class Chat(AbstractEntity):
    json = JSONField(default=dict)


class Offer(AbstractEntity):
    description = models.TextField(default='Description')
    status = models.CharField(choices=OfferStatusField, default='PENDING', max_length=50)
    date = models.DateTimeField(default=timezone.now)
    hours = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.5'))])
    price = models.DecimalField(max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal('1.0'))])
    currency = models.CharField(default='EUR', max_length=3)
    paymentCode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    paymentPackage = models.ForeignKey(PaymentPackage, related_name='offers', on_delete=models.PROTECT)
    eventLocation = models.ForeignKey(EventLocation, related_name='offers', on_delete=models.PROTECT)
    reason = models.TextField(blank=True, null=True)
    appliedVAT = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.0'))])
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.OneToOneField(Rating, on_delete=models.SET_NULL, null=True, blank=True)
    chat = models.OneToOneField(Chat, related_name='offer', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.description)


class SystemConfiguration(AbstractEntity):
    minimumPrice = models.DecimalField(default=0.0, max_digits=20, decimal_places=2,
                                       validators=[MinValueValidator(Decimal('1.0'))])
    currency = models.CharField(default='EUR', max_length=3)
    paypalTax = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.0'))])
    creditCardTax = models.DecimalField(max_digits=3, decimal_places=1,
                                        validators=[MinValueValidator(Decimal('0.0'))])
    vat = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.0'))])
    profit = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.0'))])
    corporateEmail = models.EmailField(default='info@grooving.com')
    reportEmail = models.EmailField(default='report@grooving.com')
    logo = models.CharField(max_length=500)
    appName = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255, blank=True, null=True)
    termsText_es = models.TextField(default='Terms text')
    termsText_en = models.TextField(default='Texto de terminos')
    privacyText_es = models.TextField(default='Privacy text')
    privacyText_en = models.TextField(default='Texto de privacidad')
    aboutUs_es = models.TextField(default='About Us')
    aboutUs_en = models.TextField(default='Sobre nosotros')
