from django.contrib.auth.models import User, Group
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from Grooving.models import Artist, Portfolio, PortfolioModule, ModuleTypeField
from utils.Assertions import Assertions
from urllib.parse import urlparse
from utils.utils import check_accept_language
from .internationalization import translate
from utils.authentication_utils import get_logged_user


class PortfolioModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioModule
        fields = ('type', 'link', 'description', 'portfolio')

    # Esto sobrescribe una función heredada del serializer.
    def save(self, pk=None, logged_user=None):
        module = PortfolioModule()
        if self.initial_data.get('id') is None and pk is None:
            # creation
            module = self._service_create(self.initial_data, module)
        else:
             # edit
            id = (self.initial_data, pk)[pk is not None]
            module = PortfolioModule.objects.filter(pk=id).first()
            module = self._service_update(self.initial_data, module)
        return module

    # Se pondrá service delante de nuestros métodos para no sobrescribir por error métodos del serializer
    @staticmethod
    def _service_create(json: dict, module: PortfolioModule):
        module.type = json.get('type')
        module.link = json.get('link')
        module.description = json.get('description')
        module.portfolio_id = json.get('portfolio')
        module.save()
        return module

    @staticmethod
    def _service_update(json: dict, module: PortfolioModule):
        module.type = json.get('type')
        module.link = json.get('link')
        module.description = json.get('description')
        module.portfolio_id = json.get('portfolio')
        module.save()
        return module

    def validate(self, attrs):

        language = check_accept_language(attrs)

        # Artist validation

        language = check_accept_language(attrs)

        Assertions.assert_true_raise400(attrs, translate(language, "ERROR_NO_DATA_GIVEN"))

        artist = Artist.objects.filter(user_id=attrs.user.id).first()

        Assertions.assert_true_raise403(artist, translate(language, 'ERROR_USER_FORBIDDEN'))

        # Body request validation

        json = attrs.data

        Assertions.assert_true_raise400(json.get("type"),
                                        translate(language, 'ERROR_FIELD_TYPE'))
        Assertions.assert_true_raise400(json.get("link"),
                                        translate(language, 'ERROR_FIELD_LINK'))
        Assertions.assert_true_raise400(json.get("description"),
                                        translate(language, 'ERROR_FIELD_DESCRIPTION'))
        Assertions.assert_true_raise400(json.get("portfolio"),
                                        translate(language, 'ERROR_FIELD_PORTFOLIO'))

        # type validation

        Assertions.assert_true_raise400(dict(ModuleTypeField).get(json.get("type")),
                                        translate(language, 'ERROR_NOTFOUND_TYPE'))

        # link validation

        try:
            validate_url = URLValidator(schemes=['http', 'https'])
            validate_url(json.get('link'))
            link = urlparse(json.get('link'))

            if json.get("type") == 'VIDEO':
                Assertions.assert_true_raise400(link.netloc == 'www.youtube.com' or link.netloc == 'm.youtube.com',
                                                translate(language, 'ERROR_NOTVALID_LINK'))
            elif json.get("type") == 'TWITTER':
                Assertions.assert_true_raise400(link.netloc == 'twitter.com' or link.netloc == 'mobile.twitter.com',
                                                translate(language, 'ERROR_NOTVALID_LINK'))
            elif json.get("type") == 'INSTAGRAM':
                Assertions.assert_true_raise400(link.netloc == 'www.instagram.com',
                                                translate(language, 'ERROR_NOTVALID_LINK'))

        except ValidationError:
            Assertions.assert_true_raise400(False,
                                            translate(language, 'ERROR_NOTVALID_LINK'))
        # Portfolio validation

        portfolio = Portfolio.objects.filter(pk=json.get("portfolio")).first()

        Assertions.assert_true_raise400(portfolio,
                                        translate(language, 'ERROR_NOTFOUND_PORTFOLIO'))

        if json.get('type') == 'TWITTER':
            moduleTwitter = PortfolioModule.objects.filter(portfolio=portfolio, type='TWITTER').first()
            Assertions.assert_true_raise400(moduleTwitter is None,
                                            translate(language, 'ERROR_CREATEMODULE_TWITTER'))
        if json.get('type') == 'INSTAGRAM':
            moduleInstagram = PortfolioModule.objects.filter(portfolio=portfolio, type='INSTAGRAM').first()
            Assertions.assert_true_raise400(moduleInstagram is None and json.get('type') == 'INSTAGRAM',
                                            translate(language, 'ERROR_CREATEMODULE_INSTAGRAM'))

        # User owner validation

        Assertions.assert_true_raise400(portfolio.artist.user.id == attrs.user.id,
                                        translate(language, 'ERROR_REFERENCE_PORTFOLIO'))
        return True





