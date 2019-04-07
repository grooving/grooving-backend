from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, Calendar, ArtisticGender, PortfolioModule, Zone, PaymentPackage, Artist
from utils.Assertions import Assertions
import re


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

    #parentGender = ParentGenderSerializer(read_only=True)

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender')


class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Zone
        fields = ('name', 'parentZone')


class PaymentPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description')


class PortfolioModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioModule
        fields = ('type', 'link')


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):

    artisticName = serializers.CharField()
    biography = serializers.CharField()
    banner = serializers.CharField()
    images = serializers.SerializerMethodField('list_images')
    videos = serializers.SerializerMethodField('list_videos')
    main_photo = serializers.SerializerMethodField('list_photo')
    #artisticGenders = serializers.SerializerMethodField('list_genders')
    artist = ArtistSerializer(read_only=True)
    zone = ZoneSerializer(read_only=True)
    artisticGender = ArtisticGenderSerializer(read_only=True, many=True)

    class Meta:
        model = Portfolio

        fields = ('id', 'artisticName', 'biography', 'banner', 'images', 'videos', 'main_photo', 'artisticGender',
                  'artist', 'zone')

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

    @staticmethod
    def list_genders(self):

        genders = ArtisticGender.objects.filter(portfolio=self)
        genderlist = []
        for gender in genders:
            genderlist.append(gender.name)
        return genderlist

    @staticmethod
    def list_artist(self):

        artist = Artist.objects.filter(portfolio=self).first()
        artistId = artist.id

        return artistId

    def save(self, loggedUser):

        if Portfolio.objects.filter(pk=self.initial_data.get('id')).first():
            portfolio = Portfolio.objects.filter(pk=self.initial_data.get('id')).first()
            if loggedUser.portfolio.id == portfolio.id:
                portfolio = self._service_update(self.initial_data, portfolio)
                portfolio.save()
                return portfolio
            else:
                return Assertions.assert_true_raise403(False, {'error': 'User doesnt own this portfolio'})
        else:
            return Assertions.assert_true_raise404(False)

    @staticmethod
    def _service_update(json: dict, portfolio_in_db):

        Assertions.assert_true_raise400(portfolio_in_db is not None, {'error' : 'Portfolio not in database'})

        if json['artisticName'] is not None:
            portfolio_in_db.artisticName = json.get('artisticName')

        if json['banner'] is not None:
            portfolio_in_db.banner = json.get('banner')

        if json['biography'] is not None:
            portfolio_in_db.biography = json.get('biography')

        if json['images'] is not None:
            for image_db in PortfolioModule.objects.filter(type='PHOTO', portfolio=portfolio_in_db):
                aux = True
                for image in json['images']:
                    if image_db.link == image:
                        aux = False
                if aux:
                    image_db.delete()

            for image in json['images']:
                aux = True
                for image_db in PortfolioModule.objects.filter(type='PHOTO', portfolio=portfolio_in_db):
                    if image_db.link == image:
                        aux = False
                if aux:
                    Assertions.assert_true_raise400(image.endswith(".png") or image.endswith(".gif") or image.endswith(".jpg") or image.endswith(".jpeg"), {'error': 'Formato imagen erroneo'})
                    module = PortfolioModule()
                    module.type = 'PHOTO'
                    module.link = image
                    module.portfolio = portfolio_in_db
                    module.save()

        if json['videos'] is not None:

            r = re.compile('^(http(s)?:\/\/)?(|((m).)|((w){3}.))?youtu(be|.be)?(\.)')

            for video in json['videos']:
                print(video)
                Assertions.assert_true_raise400(r.match(video), {'video': 'Bad format.'})

            for video_db in PortfolioModule.objects.filter(type='VIDEO', portfolio=portfolio_in_db):
                aux = True
                for video in json['videos']:
                    if video_db.link == video:
                        aux = False
                if aux:
                    video_db.delete()

            for video in json['videos']:
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
                if genre.name in json['artisticGenders']:
                    None
                else:
                    portfolio_in_db.artisticGender.remove(genre.id)

            for genre in json['artisticGenders']:
                try:
                    genre_db = ArtisticGender.objects.get(name=genre)
                except:
                    return Assertions.assert_true_raise400(False, {'error': 'Genre not in database'})
                if portfolio_in_db.id in genre_db.portfolio_set.all():
                    None
                else:
                    portfolio_in_db.artisticGender.add(genre_db.id)

        if json['main_photo'] is not None:
            artist = Artist.objects.get(portfolio=portfolio_in_db)
            artist.photo = json['main_photo']
            artist.save()

        return portfolio_in_db


class ShortPortfolioSerializer(serializers.ModelSerializer):

    artisticGender = ArtisticGenderSerializer(read_only=True, many=True)

    class Meta:

        model = Portfolio
        fields = ('artisticName', 'artisticGender')


