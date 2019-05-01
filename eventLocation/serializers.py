from utils.Assertions import assert_true, Assertions
from rest_framework import serializers
from Grooving.models import EventLocation, Zone, Customer
from utils.utils import check_accept_language
from .internationalization import translate


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('name', 'parentZone')


class ShortEventLocationSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)

    class Meta:
        model = EventLocation
        fields = ('id', 'zone', 'customer_id')


class EventLocationSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)
    zone_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Zone.objects.all(),
                                                           source='zone')

    class Meta:
        model = EventLocation
        fields = ('id', 'name', 'address', 'equipment', 'description', 'zone', 'zone_id', 'customer_id')

    # Esto sobrescrive una función heredada del serializer.
    def save(self, userId, pk=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            eventLocation = EventLocation()
            eventLocation = self._service_create(self.initial_data, userId, eventLocation)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]

            eventLocation = EventLocation.objects.filter(pk=id).first()
            eventLocation = self._service_update(self.initial_data, eventLocation)

        return eventLocation

    # Se pondrá service delante de nuestros métodos para no sobrescribir por error métodos del serializer
    @staticmethod
    def _service_create(json: dict, userId, eventLocation: EventLocation):
        eventLocation.name = json.get('name')
        eventLocation.address = json.get('address')
        eventLocation.equipment = json.get('equipment')
        eventLocation.description = json.get('description')
        eventLocation.zone = Zone.objects.filter(pk=json.get('zone_id')).first()
        eventLocation.customer = Customer.objects.filter(user_id=userId).first()
        eventLocation.save()
        return eventLocation

    def _service_update(self, json: dict, offer_in_db: EventLocation):
        assert_true(offer_in_db, "Zone provided hasn't been found")
        offer = self._service_update_status(json, offer_in_db)

        return offer

    def validate(self, request):

        language = check_accept_language(request)

        customer = Customer.objects.filter(user_id=request.user.id).first()

        Assertions.assert_true_raise403(customer, translate(language, 'ERROR_CUSTOMER_NOT_FOUND'))

        json = request.data

        Assertions.assert_true_raise400(json.get("address"), translate(language, 'ERROR_ADDRESS_NOT_PROVIDED'))

        Assertions.assert_true_raise400(json.get("zone_id"), translate(language, 'ERROR_ZONE_NOT_PROVIDED'))

        zone: Zone = Zone.objects.filter(pk=json.get("zone_id")).first()

        Assertions.assert_true_raise400(zone, translate(language, 'ERROR_ZONE_NOT_FOUND'))

        Assertions.assert_true_raise400(zone.zone_set.count() == 0, translate(language, 'ERROR_ZONE_CAN_NOT_ASSIGNED'))

        return True
