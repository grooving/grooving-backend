from rest_framework import serializers
from Grooving.models import Zone
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from adminBoard.internationalization import translate


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('name', 'parentZone')

    def save(self, request):

        zone = self._service_create_zone(self.initial_data, request)
        return zone

    def update(self, request, pk):

        zone = self._service_update_zone(self.initial_data, request, pk)
        return zone

    @staticmethod
    def _service_update_zone(json: dict, request, pk):
        language = check_accept_language(request)
        Assertions.assert_true_raise400(json,
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_EMPTY_FORM_NOT_VALID"))
        zone = Zone.objects.get(pk=pk)
        zone.name = json.get('name')

        parentZone = Zone.objects.get(pk=json.get('parentZone'))
        Assertions.assert_true_raise400(parentZone, translate(keyLanguage=language,
                                                              keyToTranslate="ERROR_PARENT_ZONE_DOES_NOT_EXIST"))
        zone.parentZone = parentZone

        Assertions.assert_true_raise400(zone.name or zone.name != "",
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_ZONE_NAME_NOT_PROVIDED"))
        Assertions.assert_true_raise400(zone.parentZone or zone.parentZone != "",
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_PARENT_ZONE_NOT_PROVIDED"))

        parentZone = Zone.objects.get(pk=zone.parentZone_id)

        if parentZone:
            grandfather_zone = parentZone.parentZone
            if grandfather_zone:
                grandfather_zone = Zone.objects.get(pk=grandfather_zone.id)
                id = grandfather_zone.parentZone
                Assertions.assert_true_raise400(id is None,
                                                translate(keyLanguage=language,
                                                          keyToTranslate="ERROR_ZONE_MORE_THAN_3_LEVELS"))

        try:
            zone.save()
            return zone
        except Zone.DoesNotExist:
            Assertions.assert_true_raise400(False, translate(keyLanguage=language,
                                                             keyToTranslate="ERROR_ZONE_NOT_FOUND"))

    @staticmethod
    def _service_create_zone(json: dict, request):
        language = check_accept_language(request)
        name = json.get('name')
        parentZone = Zone.objects.get(pk=json.get('parentZone'))
        Assertions.assert_true_raise400(parentZone, translate(keyLanguage=language,
                                                              keyToTranslate="ERROR_PARENT_ZONE_DOES_NOT_EXIST"))
        if parentZone:
            grandfather_zone = parentZone.parentZone
            if grandfather_zone:
                grandfather_zone = Zone.objects.get(pk=grandfather_zone.id)
                id = grandfather_zone.parentZone
                Assertions.assert_true_raise400(id is None,
                                                translate(keyLanguage=language,
                                                          keyToTranslate="ERROR_ZONE_MORE_THAN_3_LEVELS"))
        names = list(Zone.objects.values_list('name', flat=True))
        Assertions.assert_true_raise400(name not in names, translate(keyLanguage=language,
                                                                     keyToTranslate="ERROR_ZONE_ALREADY_EXISTS"))

        zone = Zone.objects.create(name=json.get('name'), parentZone=parentZone)

        return zone

    @staticmethod
    def validate_zone(request):
        language = check_accept_language(request)

        parentzonesid = list(Zone.objects.values_list('id', flat=True))
        name = request.data.get("name").strip()
        parentzone = request.data.get("parentZone")

        Assertions.assert_true_raise400(parentzone, translate(keyLanguage=language,
                                                                          keyToTranslate="ERROR_PARENT_ZONE_DOES_NOT_EXIST"))
        Assertions.assert_true_raise400(request.data, translate(keyLanguage=language,
                                                                          keyToTranslate="ERROR_EMPTY_FORM_NOT_VALID"))
        Assertions.assert_true_raise400(name, translate(keyLanguage=language,
                                                             keyToTranslate="ERROR_ZONE_NAME_NOT_PROVIDED"))



        Assertions.assert_true_raise400(int(parentzone) in parentzonesid, translate(keyLanguage=language,
                                                             keyToTranslate="ERROR_PARENT_ZONE_DOES_NOT_EXIST"))
        Assertions.assert_true_raise400(len(name) > 1, translate(keyLanguage=language,
                                                             keyToTranslate="ERROR_ZONE_NAME_TOO_SHORT"))

        return True
