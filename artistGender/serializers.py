from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, ArtisticGender
from utils.Assertions import Assertions


class ArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender', 'portfolio_set')


class ShortArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name')


class SearchGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender')

    @staticmethod
    def _get_parent_of_all():
        parent_of_all = ArtisticGender.objects.filter(parentGender=None).first()
        return parent_of_all

    @staticmethod
    def get_tree():
        parent = SearchGenreSerializer._get_parent_of_all()
        Assertions.assert_true_raise404(parent, "Parent zone not found")
        return SearchGenreSerializer._get_childs_genre(parent, [])[0]

    @staticmethod
    def get_base_childs(genre, total=[]):
        total = total
        total.append(genre)
        base_childs = []
        for child_genre in genre.artisticgender_set.all():
            if child_genre not in total:
                recursive_data = SearchGenreSerializer.get_base_childs(child_genre, total)

                total = recursive_data[1]
                if child_genre.artisticgender_set.all().count() == 0:
                    base_childs.append(child_genre)
                else:
                    base_childs.extend(recursive_data[0])

        if len(base_childs) == 0:
            base_childs.append(genre)

        return base_childs, total

    @staticmethod
    def _get_childs_genre(genre, total=[]):
        total = total
        total.append(genre)
        id = str(genre.id)
        name = genre.name
        parentGenre = None
        if genre.parentGender is not None:
            parentGenre = str(genre.parentGender.id)

        child_dicts_list = []
        for child_genre in genre.artisticgender_set.all():
            if child_genre not in total:
                recursive_data = SearchGenreSerializer._get_childs_genre(child_genre, total)
                total = recursive_data[1]
                child_dicts_list.append(recursive_data[0])

        dictionary = {"id": id, "name": name, "parent": parentGenre, "children": child_dicts_list}

        return dictionary, total
