from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, ArtisticGender
from utils.Assertions import Assertions


class ArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender')

    def save(self, pk=None, logged_user=None):

        if self.initial_data.get('id') is None and pk is None:
            genre = ArtisticGender()
            genre = self._service_create(self.initial_data, genre)
            genre.save()
            Assertions.assert_true_raise401(genre,{'error': 'ERROR_IN_CREATION'})
            return genre
        else:

            id_genre = (self.initial_data.get('id'), pk)[pk is not None]

            genre_id_control = str(self.initial_data.get('id'))

            Assertions.assert_true_raise400(genre_id_control.isdigit(), {'error': 'ERROR_INCORRECT_ID'})

            genre = ArtisticGender.objects.filter(pk=id_genre).first()
            genre = self._service_update(self.initial_data, genre)
            genre.save()
            return genre

    @staticmethod
    def _service_create(json: dict, genre: ArtisticGender):

        Assertions.assert_true_raise401(ArtisticGender.objects.filter(name=json.get('name')).first() is None, {'error': 'ERROR_GENRE_EXISTS'})

        genre.name = json.get('name')

        Assertions.assert_true_raise401(ArtisticGender.objects.filter(id=json.get('parentGender')).first(),
                                        {'error': 'ERROR_GENRE_DOESNT_EXIST'})

        genre.parentGender = ArtisticGender.objects.filter(id=json.get('parentGender')).first()

        genre.save()

        return genre

    @staticmethod
    def _service_update(json: dict, genre: ArtisticGender):

        genre_id_control = str(json.get('id'))

        Assertions.assert_true_raise400(genre_id_control.isdigit(), {'error': 'ERROR_INCORRECT_ID'})

        try:
            genre = ArtisticGender.objects.get(pk=json.get('id'))
        except ArtisticGender.DoesNotExist:
            Assertions.assert_true_raise400(genre, {'error': 'ERROR_INCORRECT_ID'})


        # Se busca si un artisticGenre con el nombre pedido ya existe

        genre_name_control = ArtisticGender.objects.filter(name=json.get('name')).first()

        # Es posible que sólo se quiera cambiar el parent, asi que es necesario ver si el genre con ese nombre y el que estamos editando son el mismo

        if genre_name_control is not None and genre_name_control.id != json.get('id'):
            # Si tienen el mismo nombre y son distintos... ¡tenemos un problema! Levantamos excepción.
            Assertions.assert_true_raise400(ArtisticGender.objects.filter(name=json.get('name')).first() is None,
                                            {'error': 'ERROR_GENRE_EXISTS'})

        Assertions.assert_true_raise400(json.get('name') != '',
                                        {'error': 'ERROR_GENRE_NULL_NAME'})

        Assertions.assert_true_raise400(json.get('name') is not None,
                                        {'error': 'ERROR_GENRE_NULL_NAME'})

        parentGender_control = str(json.get('parentGender'))

        Assertions.assert_true_raise400(parentGender_control.isdigit(), {'error': 'ERROR_NO_PARENT_GENRE_ID'})

        Assertions.assert_true_raise404(ArtisticGender.objects.filter(id=json.get('parentGender')).first(),
                                        {'error': 'ERROR_PARENT_GENRE_NOT_FOUND'})

        genre.name = json.get('name')

        genre.parentGender = ArtisticGender.objects.filter(id=json.get('parentGender')).first()

        genre.save()

        return genre


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
        Assertions.assert_true_raise404(parent, {'error', 'Parent zone not found'})
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

    @staticmethod
    def get_children(parentId = None):

        if parentId is None:
            parent = SearchGenreSerializer._get_parent_of_all()
            Assertions.assert_true_raise404(parent, {'error', 'Parent zone not found'})

            name = parent.name
        else:
            parent = ArtisticGender.objects.filter(id=parentId).first()

            name = parent.name

        child_dicts_list = ArtisticGender.objects.filter(parentGender=parent)
        children = []

        for child in child_dicts_list:
            childdict = {"id": child.id, "name": child.name}
            children.append(childdict)

        dictionary = {"id": parentId, "name": name, "children": children}

        return dictionary
