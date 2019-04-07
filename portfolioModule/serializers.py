from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from Grooving.models import Artist, Portfolio, PortfolioModule, ModuleTypeField
from utils.Assertions import Assertions
from urllib.parse import urlparse

class PortfolioModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioModule
        fields = ('type', 'link', 'description', 'portfolio')

    # Esto sobrescribe una función heredada del serializer.
    def save(self, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            module = PortfolioModule()
            module = self._service_create(self.initial_data, module, logged_user)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]

            module = PortfolioModule.objects.filter(pk=id).first()
            module = self._service_update(self.initial_data, module, logged_user)

        return module

    # Se pondrá service delante de nuestros métodos para no sobrescribir por error métodos del serializer
    @staticmethod
    def _service_create(json: dict, module: PortfolioModule, logged_user: User):
        module.type = json.get('type')
        module.link = json.get('link')
        module.description = json.get('description')
        module.portfolio_id = json.get('portfolio')
        module.save()
        return module

    def validate(self, attrs):

        # Artist validation

        artist = Artist.objects.filter(user_id=attrs.user.id).first()

        Assertions.assert_true_raise403(artist, {'error': 'user isn\'t authorized'})

        # Body request validation

        json = attrs.data

        Assertions.assert_true_raise400(json.get("type"),
                                        {'error': 'type field not provided'})
        Assertions.assert_true_raise400(json.get("link"),
                                        {'error': 'link field not provided'})
        Assertions.assert_true_raise400(json.get("description"),
                                        {'error': 'description field not provided'})
        Assertions.assert_true_raise400(json.get("portfolio"),
                                        {'error': 'portfolio field not provided'})

        # type validation

        Assertions.assert_true_raise400(dict(ModuleTypeField).get(json.get("type")),
                                        {'error': 'type field not found'})

        # link validation

        try:
            validate_url = URLValidator(schemes=('http', 'https'))
            validate_url(json.get('link'))
            link = urlparse(json.get('link'))

            if json.get("type") == 'VIDEO':
                Assertions.assert_true_raise400(link.netloc == 'www.youtube.com' or link.netloc == 'm.youtube.com',
                                                {'error': 'link field not valid for ' + json.get("type")})
            elif json.get("type") == 'FACEBOOK':
                Assertions.assert_true_raise400(link.netloc == 'www.facebook.com' or link.netloc == 'm.facebook.com',
                                                {'error': 'link field not valid for ' + json.get("type")})
            elif json.get("type") == 'INSTAGRAM':
                Assertions.assert_true_raise400(link.netloc == 'www.instagram.com',
                                                {'error': 'link field not valid for ' + json.get("type")})

        except ValidationError:
            Assertions.assert_true_raise400(False,
                                            {'error': 'link field not valid'})
        # Portfolio validation

        portfolio = Portfolio.objects.filter(pk=json.get("portfolio")).first()

        Assertions.assert_true_raise400(portfolio,
                                        {'error': 'portfolio doesn\'t exist'})

        moduleFacebook = PortfolioModule.objects.filter(portfolio=portfolio, type='FACEBOOK').first()
        Assertions.assert_true_raise400(moduleFacebook is None and json.get('type') == 'FACEBOOK',
                                        {'error': 'can\'t create other FACEBOOK module'})

        moduleInstagram = PortfolioModule.objects.filter(portfolio=portfolio, type='INSTRAGRAM').first()
        Assertions.assert_true_raise400(moduleInstagram is None and json.get('type') == 'INSTAGRAM',
                                        {'error': 'can\'t create other INSTAGRAM module'})

        # User owner validation

        Assertions.assert_true_raise400(portfolio.artist.user.id == attrs.user.id,
                                        {'error': 'can\'t reference this portfolio'})
        return True





