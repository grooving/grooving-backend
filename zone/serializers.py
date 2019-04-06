from rest_framework import serializers
from Grooving.models import Zone
from utils.Assertions import Assertions


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('id', 'name', 'parentZone', 'portfolio_set')


class SearchZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('id', 'name', 'parentZone')

    @staticmethod
    def _get_parent_of_all():
        parent_of_all = Zone.objects.filter(parentZone=None).first()
        return parent_of_all

    @staticmethod
    def get_tree():
        parent = SearchZoneSerializer._get_parent_of_all()
        Assertions.assert_true_raise404(parent is not None)
        return SearchZoneSerializer._get_childs_zone(parent, [])[0]

    @staticmethod
    def _get_childs_zone(zone, total=[]):
        total = total
        total.append(zone)
        id = str(zone.id)
        name = zone.name
        child_dicts_list = []
        for child_zone in zone.zone_set.all():
            if child_zone not in total:
                recursive_data = SearchZoneSerializer._get_childs_zone(child_zone, total)
                total = recursive_data[1]
                child_dicts_list.append(recursive_data[0])

        dictionary = {"id": id, "name": name, "children": child_dicts_list}

        return dictionary, total


