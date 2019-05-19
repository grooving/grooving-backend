from Grooving.models import Actor, Artist, Customer, Admin
from rest_framework import serializers
from utils.Assertions import Assertions


class LanguageChooserArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('language',)

    def validate(self, attrs):

        language = attrs.query_params.get('lang')

        Assertions.assert_true_raise400(language, {'error': 'ERROR_NO_LANGUAGE_GIVEN'})

        Assertions.assert_true_raise400(language.isalpha(), {'error': 'ERROR_NO_MATCHING_LANGUAGE'})

        language = language.lower()

        Assertions.assert_true_raise400(language == 'es' or language == 'en', {'error': 'ERROR_NO_MATCHING_LANGUAGE'})

        return True

    def save(self, pk=None, logged_user=None):

        id = (self.initial_data, pk)[pk is not None]

        actor = Actor.objects.filter(pk=id).first()
        actor = self._service_update(self.initial_data, actor, logged_user)

        return actor

    def _service_update(self, json: dict, actor: Actor):
        Assertions.assert_true_raise400(actor, {'error': 'ERROR_ACTOR_NOT_FOUND'})

        lang = json.get('lang')

        actor.language = lang

        actor.save()

        return actor


class LanguageChooserCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('language',)

    def validate(self, attrs):

        language = attrs.query_params.get('lang')

        Assertions.assert_true_raise400(language, {'error': 'ERROR_NO_LANGUAGE_GIVEN'})

        Assertions.assert_true_raise400(language.isalpha(), {'error': 'ERROR_NO_MATCHING_LANGUAGE'})

        language = language.lower()

        Assertions.assert_true_raise400(language == 'es' or language == 'en', {'error': 'ERROR_NO_MATCHING_LANGUAGE'})

        return True

    def save(self, pk=None, logged_user=None):

        id = (self.initial_data, pk)[pk is not None]

        actor = Actor.objects.filter(pk=id).first()
        actor = self._service_update(self.initial_data, actor, logged_user)

        return actor

    def _service_update(self, json: dict, actor: Actor):
        Assertions.assert_true_raise400(actor, {'error': 'ERROR_ACTOR_NOT_FOUND'})

        lang = json.get('lang')

        actor.language = lang

        actor.save()

        return actor


class LanguageChooserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('language',)

    def validate(self, attrs):

        language = attrs.query_params.get('lang')

        Assertions.assert_true_raise400(language, {'error': 'ERROR_NO_LANGUAGE_GIVEN'})

        Assertions.assert_true_raise400(language.isalpha(), {'error': 'ERROR_NO_MATCHING_LANGUAGE'})

        language = language.lower()

        Assertions.assert_true_raise400(language == 'es' or language == 'en', {'error': 'ERROR_NO_MATCHING_LANGUAGE'})

        return True

    def save(self, pk=None, logged_user=None):

        id = (self.initial_data, pk)[pk is not None]

        actor = Admin.objects.filter(pk=id).first()
        actor = self._service_update(self.initial_data, actor, logged_user)

        return actor

    def _service_update(self, json: dict, actor: Admin):
        Assertions.assert_true_raise400(actor, {'error': 'ERROR_ACTOR_NOT_FOUND'})

        lang = json.get('lang')

        actor.language = lang

        actor.save()

        return actor
