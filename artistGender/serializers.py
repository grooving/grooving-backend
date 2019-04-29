from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, ArtisticGender
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from .internationalization import translate
from utils.authentication_utils import get_artist_or_customer_by_user
from .internationalization import translate


class ArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name_es', 'name_en', 'parentGender')


    def save(self, pk=None, logged_user=None, language = None):

        if self.initial_data.get('id') is None and pk is None:
            genre = ArtisticGender()
            genre = self._service_create(self.initial_data, genre, language)
            genre.save()
            Assertions.assert_true_raise401(genre, translate(language, 'ERROR_IN_CREATION'))
            return genre
        else:

            id_genre = (self.initial_data.get('id'), pk)[pk is not None]
            genre_id_control = str(self.initial_data.get('id'))

            genre = ArtisticGender.objects.filter(pk=id_genre).first()
            genre = self._service_update(self.initial_data, genre, logged_user, language)
            genre.save()
            return genre

    @staticmethod
    def _service_create(json: dict, genre: ArtisticGender, language):

        Assertions.assert_true_raise401(ArtisticGender.objects.filter(name=json.get('name')).first() is None, translate(language, 'ERROR_GENRE_EXISTS'))
        Assertions.assert_true_raise401(json.get('name') != "",translate(language, 'ERROR_GENRE_NULL_NAME'))
        Assertions.assert_true_raise401(json.get('name') is not None, translate(language, 'ERROR_GENRE_NULL_NAME'))

        genre.name_en = json.get('name_en')
        genre.name_es = json.get('name_es')

        if json.get('parentGender') is not None:
            Assertions.assert_true_raise401(ArtisticGender.objects.filter(id=json.get('parentGender')).first() is not None,
                                        translate(language, 'ERROR_GENRE_DOESNT_EXIST'))

        genre.parentGender = ArtisticGender.objects.filter(id=json.get('parentGender')).first()

        genre.save()

        return genre

    @staticmethod
    def _service_update(json: dict, genre: ArtisticGender, loggedUser: User):

        user = get_artist_or_customer_by_user(loggedUser)
        language = user.language

        genre_id_control = str(json.get('id'))

        Assertions.assert_true_raise400(genre_id_control.isdigit(), translate(language, 'ERROR_INCORRECT_ID'))

        try:
            genre = ArtisticGender.objects.get(pk=json.get('id'))
        except ArtisticGender.DoesNotExist:
            Assertions.assert_true_raise404(False, translate(language, "ERROR_ARTISTIC_GENRE_NOT_FOUND"))


        # Se busca si un artisticGenre con el nombre pedido ya existe

        genre_name_control = ArtisticGender.objects.filter(name_es=json.get('name_es')).first()

        # Es posible que sólo se quiera cambiar el parent, asi que es necesario ver si el genre con ese nombre y el que estamos editando son el mismo

        if genre_name_control is not None and genre_name_control.id != json.get('id'):
            # Si tienen el mismo nombre y son distintos... ¡tenemos un problema! Levantamos excepción.
            Assertions.assert_true_raise400(ArtisticGender.objects.filter(name_es=json.get('name_es')).first() is None,
                                           translate(language, 'ERROR_GENRE_EXISTS'))

        Assertions.assert_true_raise400(json.get('name_es') != '',
                                        translate(language, 'ERROR_GENRE_NULL_NAME'))

        Assertions.assert_true_raise400(json.get('name_es') is not None,
                                        translate(language, 'ERROR_GENRE_NULL_NAME'))

        Assertions.assert_true_raise400(json.get('name_en') != '',
                                        translate(language, 'ERROR_GENRE_NULL_NAME'))

        Assertions.assert_true_raise400(json.get('name_en') is not None,
                                        translate(language, 'ERROR_GENRE_NULL_NAME'))

        parentGender_control = str(json.get('parentGender'))

        Assertions.assert_true_raise400(parentGender_control.isdigit(), translate(language,'ERROR_NO_PARENT_GENRE_ID'))

        Assertions.assert_true_raise404(ArtisticGender.objects.filter(id=json.get('parentGender')).first(),
                                        translate(language, 'ERROR_PARENT_GENRE_NOT_FOUND'))

        genre.name_en = json.get('name_en')
        genre.name_es = json.get('name_es')

        genre.parentGender = ArtisticGender.objects.filter(id=json.get('parentGender')).first()

        genre.save()

        return genre


class ShortArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name')


class SearchGenreSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender')

    def get_name(self, obj):

        genre = ArtisticGender.objects.filter(id=obj.id).first()

        language = self.context.get("language")
        print(language)
        if language == "es":
            name = genre.name_es
        elif language == "en":
            name = genre.name_en

        return name

    @staticmethod
    def _get_parent_of_all():
        parent_of_all = ArtisticGender.objects.filter(parentGender=None).first()
        return parent_of_all

    @staticmethod
    def get_tree(language):
        parent = SearchGenreSerializer._get_parent_of_all()
        Assertions.assert_true_raise404(parent, translate(language, 'ERROR_PARENT_GENRE_NOT_FOUND'))
        return SearchGenreSerializer._get_childs_genre(language,parent, [])[0]

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
    def _get_childs_genre(language, genre, total=[]):
        total = total
        total.append(genre)
        id = str(genre.id)

        if language == "es":
            name = genre.name_es
        elif language == "en":
            name = genre.name_en

        parentGenre = None
        if genre.parentGender is not None:
            parentGenre = str(genre.parentGender.id)

        child_dicts_list = []
        for child_genre in genre.artisticgender_set.all():
            if child_genre not in total:
                recursive_data = SearchGenreSerializer._get_childs_genre(language,child_genre, total)
                total = recursive_data[1]
                child_dicts_list.append(recursive_data[0])

        dictionary = {"id": id, "name": name, "parent": parentGenre, "children": child_dicts_list}

        return dictionary, total

    @staticmethod
    def get_children(language,parentId = None):

        Assertions.assert_true_raise401(language is not None, translate(language, 'ERROR_NO_GIVEN_LANGUAGE'))

        if parentId is None:
            parent = SearchGenreSerializer._get_parent_of_all()
            Assertions.assert_true_raise401(parent, translate(language, 'ERROR_PARENT_GENRE_NOT_FOUND'))

            if language == "es":
                name = parent.name_es
            elif language == "en":
                name = parent.name_en
        else:
            parent = ArtisticGender.objects.filter(id=parentId).first()
            Assertions.assert_true_raise401(parent, translate(language, 'ERROR_PARENT_GENRE_NOT_FOUND'))
            if language == "es":
                name = parent.name_es
            elif language == "en":
                name = parent.name_en

        child_dicts_list = {}
        if ArtisticGender.objects.filter(parentGender=parent) is not None:
            child_dicts_list = ArtisticGender.objects.filter(parentGender=parent).order_by('name_es')

        children = []

        for child in child_dicts_list:
            name_child = ""
            if language == "es":
                name_child = child.name_es
            elif language == "en":
                name_child = child.name_en
            Assertions.assert_true_raise401(name_child != '', translate(language, 'ERROR_GENRE_NULL_NAME'))
            childdict = {"id": child.id, "name": name_child}
            children.append(childdict)

        granddadId=None
        if parent.parentGender is not None:

            grandad =  parent.parentGender
            granddadId = grandad.id

        if parent.parentGender is None:
            depth = 1

        elif grandad.parentGender is None:
            depth = 2

        else:
            depth = 3

        dictionary = {"depth": depth, "id": parentId, "name": name, "parent": granddadId, "children": children}

        return dictionary

    @staticmethod
    def get_parent_children(language,parentId = None):

        if parentId is None:
            parent = SearchGenreSerializer._get_parent_of_all()
            Assertions.assert_true_raise401(parent, translate(language, 'ERROR_PARENT_GENRE_NOT_FOUND'))

        else:
            parent = ArtisticGender.objects.filter(id=parentId).first()
            Assertions.assert_true_raise401(parent, translate(language, 'ERROR_PARENT_GENRE_NOT_FOUND'))

        if ArtisticGender.objects.filter(parentGender=parent) is not None:
            child_dicts_list = ArtisticGender.objects.filter(parentGender=parent).order_by('name_es')

        children = []

        for child in child_dicts_list:
            if language == "es":
                name_child = child.name_es
            elif language == "en":
                name_child = child.name_en
            childdict = {"id": child.id, "name": name_child}
            children.append(childdict)

        granddadId=None

        if parent.parentGender is not None:

            grandad =  parent.parentGender
            granddadId = grandad.id

        dictionary = {"id": parentId, "name_es": parent.name_es, "name_en": parent.name_en, "parent": granddadId, "children": children}

        return dictionary


class ArtisticGenderSerializerOut(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender')


    def get_name(self, obj):

        genre = ArtisticGender.objects.filter(id=obj.id).first()

        language = self.context.get("language")

        if language == "es":
            name = genre.name_es
        elif language == "en":
            name = genre.name_en

        return name
