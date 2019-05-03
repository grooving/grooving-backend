from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, Calendar, ArtisticGender, PortfolioModule, PaymentPackage, Artist, Zone
from utils.Assertions import Assertions
from artistGender.serializers import ArtisticGenderSerializerOut
import re
from utils.strings import Strings
from .internationalization import translate


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name')


class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Artist
        fields = ('id', 'rating', 'user', 'photo')


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ('days',)


'''class ParentGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisticGender
        fields = ('name',)'''


class ArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name_es', 'name_en', 'parentGender')


class PaymentPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description')


class PortfolioModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioModule
        fields = ('type', 'link')


class ZoneSerializer(serializers.ModelSerializer):

    parentZone_id = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all(), source='parentZone')

    class Meta:
        model = Zone
        fields = ('id', 'parentZone_id', 'name')


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):

    artisticName = serializers.CharField(allow_null=True)
    biography = serializers.CharField(allow_null=True)
    banner = serializers.CharField(allow_blank=True,allow_null=True)
    images = serializers.SerializerMethodField('list_images')
    videos = serializers.SerializerMethodField('list_videos')
    main_photo = serializers.SerializerMethodField('list_photo')
    artist = ArtistSerializer(read_only=True)
    language = serializers.SerializerMethodField()
    artisticGender = ArtisticGenderSerializerOut(read_only=True, many=True,context={'language': language})
    zone = ZoneSerializer(read_only=True, many=True)

    class Meta:
        model = Portfolio

        fields = ('id','language', 'artisticName', 'biography', 'banner', 'images', 'videos', 'main_photo', 'artisticGender',
                  'artist', 'zone')

    def get_language(self,obj):
        return self.context.get('language')

    @staticmethod
    def list_images(self):

        modules = PortfolioModule.objects.filter(type='PHOTO', portfolio=self)
        images = []
        for image in modules:
            images.append(image.link)

        return images

    @staticmethod
    def list_videos(self):

        modules = PortfolioModule.objects.filter(type='VIDEO', portfolio=self)
        videos = []
        for video in modules:
            videos.append(video.link)

        return videos

    @staticmethod
    def list_photo(self):

        artist = Artist.objects.filter(portfolio=self).first()
        photo = ""
        if artist.photo:
            photo = artist.photo

        return photo

    def list_genders(self,obj):

        genders = ArtisticGender.objects.filter(portfolio=obj)
        genderlist = []
        language = self.context.get("language")
        for gender in genders:
            if language == 'es':
                genderlist.append(gender.name_es)
            elif language == 'en':
                genderlist.append(gender.name_en)
        return genderlist

    @staticmethod
    def list_artist(self):

        artist = Artist.objects.filter(portfolio=self).first()
        artistId = artist.id

        return artistId

    def save(self, loggedUser, language='en'):

        if Portfolio.objects.filter(pk=self.initial_data.get('id')).first():
            portfolio = Portfolio.objects.filter(pk=self.initial_data.get('id')).first()
            if loggedUser.portfolio.id == portfolio.id:
                portfolio = self._service_update(self.initial_data, portfolio, language=language)
                portfolio.save()
                return portfolio
            else:
                return Assertions.assert_true_raise403(False, translate(language, 'ERROR_PORTFOLIO_NOT_OWNER'))
        else:
            return Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_PORTFOLIO_NOT_FOUND'))

    @staticmethod
    def _service_update(json: dict, portfolio_in_db, language='en'):

        Assertions.assert_true_raise400(portfolio_in_db is not None, translate(language, 'ERROR_PORTFOLIO_NOT_FOUND'))

        if json['artisticName'] is not None:
            Assertions.assert_true_raise400(isinstance(json['artisticName'], str), translate(language, 'ERROR_ARTISTICNAME_BAD_PROVIDED'))
            Assertions.assert_true_raise400(Strings.check_max_length(json['artisticName'], 140),
                                            translate(language, "ERROR_ARTISTICNAME_TOO_LONG"))



            portfolio_in_db.artisticName = json.get('artisticName')

        if json['banner'] is not None:
            Assertions.assert_true_raise400(isinstance(json['banner'], str), translate(language, 'ERROR_BANNER_BAD_PROVIDED'))
            Assertions.assert_true_raise400(json['banner'].startswith('http'), translate(language, 'ERROR_BANNER_NOT_VALID_URL'))
            Assertions.assert_true_raise400(Strings.url_is_an_image(json['banner']), translate(language, 'ERROR_BANNER_NOT_URL_IMAGE'))
            Assertions.assert_true_raise400(Strings.check_max_length(json['banner'], 500),
                                            translate(language, "ERROR_URL_TOO_LONG"))
            portfolio_in_db.banner = json.get('banner')

        Assertions.assert_true_raise400(json['biography'], translate(language, 'ERROR_EMPTY_BIOGRAPHY'))
        Assertions.assert_true_raise400(isinstance(json['biography'], str), translate(language, 'ERROR_BIOGRAPHY_BAD_PROVIDED'))
        Assertions.assert_true_raise400(Strings.check_max_length(json['biography'], 1000),
                                            translate(language, "ERROR_BIOGRAPHY_TOO_LONG"))
        portfolio_in_db.biography = json.get('biography')
            #portfolio_in_db.biography = json.get('biography')

        if json['images'] is not None:
            for image_db in PortfolioModule.objects.filter(type='PHOTO', portfolio=portfolio_in_db):
                aux = True
                for image in json['images']:
                    if image_db.link == image:
                        aux = False
                if aux:
                    image_db.delete()

            for image in json['images']:
                Assertions.assert_true_raise400(isinstance(image, str), translate(language, 'ERROR_IMAGE_BAD_PROVIDED'))
                Assertions.assert_true_raise400(image.startswith('http'), translate(language, 'ERROR_IMAGE_NOT_VALID_URL'))
                Assertions.assert_true_raise400(Strings.check_max_length(image, 500), translate(language, 'ERROR_IMAGE_URL_TOO_LONG'))
                aux = True
                for image_db in PortfolioModule.objects.filter(type='PHOTO', portfolio=portfolio_in_db):
                    if image_db.link == image:
                        aux = False
                if aux:
                    Assertions.assert_true_raise400(Strings.url_is_an_image(image), translate(language, 'ERROR_IMAGE_NOT_URL_IMAGE'))
                    module = PortfolioModule()
                    module.type = 'PHOTO'
                    module.link = image
                    module.portfolio = portfolio_in_db
                    module.save()

        if json['videos'] is not None:

            r = re.compile('^(http(s)?:\/\/)?(|((m).)|((w){3}.))?youtu(be|.be)?(\.)')

            for video in json['videos']:
                Assertions.assert_true_raise400(r.match(video), translate(language, 'ERROR_VIDEO_YOUTUBE'))

            for video_db in PortfolioModule.objects.filter(type='VIDEO', portfolio=portfolio_in_db):
                aux = True
                for video in json['videos']:
                    if video_db.link == video:
                        aux = False
                if aux:
                    video_db.delete()

            for video in json['videos']:
                Assertions.assert_true_raise400(isinstance(video, str), translate(language, 'ERROR_VIDEO_BAD_PROVIDED'))
                Assertions.assert_true_raise400(Strings.check_max_length(video, 500), translate(language, 'ERROR_VIDEO_URL_TOO_LONG'))
                aux = True
                for video_db in PortfolioModule.objects.filter(type='VIDEO', portfolio=portfolio_in_db):
                    if video_db.link == video:
                        aux = False
                if aux:
                    module = PortfolioModule()
                    module.type = 'VIDEO'
                    module.link = video
                    module.portfolio = portfolio_in_db
                    module.save()

        if json['artisticGenders'] is not None:

            for genre in portfolio_in_db.artisticGender.all():

                if language == 'en':
                    genre_aux = genre.name_en
                elif language == 'es':
                    genre_aux = genre.name_es
                if genre_aux in json['artisticGenders']:
                    None
                else:
                    portfolio_in_db.artisticGender.remove(genre.id)

            for genre in json['artisticGenders']:
                try:
                    if language == 'en':
                        genre_db = ArtisticGender.objects.get(name_en=genre)
                    elif language == 'es':
                        genre_db = ArtisticGender.objects.get(name_es=genre)
                except:
                    return Assertions.assert_true_raise400(False, translate(language, 'ERROR_GENRE_NOT_FOUND'))

                if portfolio_in_db.id in genre_db.portfolio_set.all():
                    None
                else:
                    portfolio_in_db.artisticGender.add(genre_db.id)

        if json['zone'] is not None:

            for zone in portfolio_in_db.zone.all():
                if zone.name in json['zone']:
                    None
                else:
                    portfolio_in_db.zone.remove(zone.id)

            for zone in json['zone']:
                try:
                    zone_db = Zone.objects.get(name=zone)
                except:
                    return Assertions.assert_true_raise400(False, translate(language, 'ERROR_ZONE_NOT_FOUND'))
                if portfolio_in_db.id in zone_db.portfolio_set.all():
                    None
                else:
                    portfolio_in_db.zone.add(zone_db.id)

        if json['main_photo'] is not None:
            Assertions.assert_true_raise400(isinstance(json['main_photo'], str), translate(language, 'ERROR_MAINPHOTO_BAD_PROVIDED'))
            Assertions.assert_true_raise400(json['main_photo'].startswith('http'), translate(language, 'ERROR_MAINPHOTO_NOT_VALID_URL'))
            Assertions.assert_true_raise400(Strings.url_is_an_image(json['main_photo']), translate(language, 'ERROR_MAINPHOTO_NOT_URL_IMAGE'))
            Assertions.assert_true_raise400(Strings.check_max_length(json['main_photo'], 500),
                                            translate(language, "ERROR_URL_TOO_LONG"))
            artist = Artist.objects.get(portfolio=portfolio_in_db)
            artist.photo = json['main_photo']
            artist.save()

        return portfolio_in_db


class ShortPortfolioSerializer(serializers.ModelSerializer):

    artisticGender = ArtisticGenderSerializer(read_only=True, many=True)

    class Meta:

        model = Portfolio
        fields = ('artisticName', 'artisticGender')
