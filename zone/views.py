from Grooving.models import Zone, Portfolio
from rest_framework.response import Response
from rest_framework import generics
from .serializers import ZoneSerializer, SearchZoneSerializer
from rest_framework import status
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user, get_user_type
from utils.Assertions import Assertions


class ZoneManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Zone.objects.get(pk=pk)
        except Zone.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            {'error': 'Zone not found'})

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        zone = self.get_object(pk)
        serializer = ZoneSerializer(zone)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        zone = self.get_object(pk)
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = ZoneSerializer(zone, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("The artisticGender is not for yourself")

    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        zone = self.get_object(pk)
        zone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateZone(generics.CreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def post(self, request, *args, **kwargs):
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = ZoneSerializer(data=request.data, partial=True)
            if serializer.validate(request.data):
                serializer.is_valid()
                zone = serializer.save()
                serialized = ZoneSerializer(zone)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied("The artisticGender is not for yourself")


class ListZones(generics.RetrieveAPIView):

    serializer_class = SearchZoneSerializer

    def get_queryset(self):

        return Zone.objects.all()

    def get(self, request, *args, **kwargs):

        tree = request.query_params.get("tree", None)
        portfolio = request.query_params.get("portfolio", None)
        zones = None
        if tree is None and portfolio is None:
            zones = list(Zone.objects.all())
            serializer = SearchZoneSerializer(zones, many=True)
            zones = serializer.data
        elif tree == "true":
            Assertions.assert_true_raise400(portfolio is None, {"error": "Portfolio's zones don't have tree option"})
            zones = SearchZoneSerializer.get_tree()
        elif portfolio is not None:

            try:
                portfolio = int(portfolio)
            except ValueError:
                Assertions.assert_true_raise400(False, {"error": "Incorrect format for id"})

            portfolio = Portfolio.objects.filter(pk=portfolio).first()
            Assertions.assert_true_raise404(portfolio,
                                            {'error':  'Portfolio not found'})
            zones = portfolio.zone.all()
            count = zones.count()
            child_zones = []
            for zone in zones:
                childs = SearchZoneSerializer.get_base_childs(zone, [])[0]
                if len(child_zones) == 0:
                    child_zones = childs
                else:
                    child_zones.extend(childs)

            serializer = SearchZoneSerializer(child_zones, many=True)
            zones = serializer.data

        return Response(zones, status=status.HTTP_200_OK)


