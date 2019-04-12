from utils.Assertions import assert_true
from rest_framework import serializers
from Grooving.models import EventLocation, Zone, Customer


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
        assert_true(offer_in_db, "No existe una oferta con esa id")
        offer = self._service_update_status(json, offer_in_db)

        return offer

    def validate(self, request):
        customer = Customer.objects.filter(user_id=request.user.id).first()
        if customer is None:
            raise serializers.ValidationError("user isn't authorized")
        json = request.data
        if json.get("address") is None:
            raise serializers.ValidationError("address field not provided")
        if json.get("zone_id") is None:
            raise serializers.ValidationError("zone_id field not provided")
        else:
            zone: Zone = Zone.objects.filter(pk=json.get("zone_id")).first()
            if zone is None:
                raise serializers.ValidationError("zone doesn't exist")
            elif zone.zone_set.count() != 0:
                raise serializers.ValidationError("zone_id " + str(zone.id) + " can't be assigned")
        return True
