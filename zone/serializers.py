from rest_framework import serializers
from Grooving.models import Zone
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from zone.internationalization import translate


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
    def get_tree(request):
        language = check_accept_language(request)
        parent = SearchZoneSerializer._get_parent_of_all()
        Assertions.assert_true_raise404(parent,translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_PARENT_ZONE_NOT_FOUND"))
        return SearchZoneSerializer._get_childs_zone(parent, [])[0]

    @staticmethod
    def get_base_childs(zone, total=[]):
        total = total
        total.append(zone)
        base_childs = []
        for child_zone in zone.zone_set.all():
            if child_zone not in total:
                recursive_data = SearchZoneSerializer.get_base_childs(child_zone, total)

                total = recursive_data[1]
                if child_zone.zone_set.all().count() == 0:
                    base_childs.append(child_zone)
                else:
                    base_childs.extend(recursive_data[0])

        if len(base_childs) == 0:
            base_childs.append(zone)

        return base_childs, total

    @staticmethod
    def _get_childs_zone(zone, total=[]):
        total = total
        total.append(zone)
        id = str(zone.id)
        name = zone.name
        parentZone = None
        if zone.parentZone is not None:
            parentZone = str(zone.parentZone.id)

        child_dicts_list = []
        for child_zone in zone.zone_set.all():
            if child_zone not in total:
                recursive_data = SearchZoneSerializer._get_childs_zone(child_zone, total)
                total = recursive_data[1]
                child_dicts_list.append(recursive_data[0])

        child_dicts_list.sort(key=lambda x: x.get("name").upper().replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U"))
        dictionary = {"id": id, "name": name, "parent": parentZone, "children": child_dicts_list}

        return dictionary, total


