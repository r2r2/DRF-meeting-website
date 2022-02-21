from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, permissions, views, filters
from rest_framework.response import Response

from dates.filters import ClientFilter
from dates.models import Follower, User
from dates.serializers import ClientCreateSerializer, ListFollowerSerializer, UserFollowerSerializer
from dates.service import watermark_image, get_location


class ClientCreateView(generics.CreateAPIView):
    """Creating User"""
    serializer_class = ClientCreateSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('image'):
            # Add watermark to uploaded image
            img = watermark_image(request.FILES['image'])
            request.data['image'] = img

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Add location
        adress = serializer.initial_data['adress']
        loc = get_location(adress)
        serializer.save(location=loc)


class ClientsFollowerView(generics.ListAPIView):
    """Display followers of user"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ListFollowerSerializer

    def get_queryset(self):
        return Follower.objects.filter(user_1=self.request.user)


class AddFollowerView(views.APIView):
    """Add to followers"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = User.objects.filter(id=pk)
        if user.exists():
            Follower.objects.create(user_2=self.request.user, user_1=user[0])
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ClientListView(generics.ListAPIView):
    """List of all users"""
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = ClientFilter
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFollowerSerializer
    queryset = User.objects.all()
    search_fields = ['distance']

    def get_queryset(self):
        qs = super().get_queryset()
        latitude = self.request.query_params.get('lat', None)
        longitude = self.request.query_params.get('lng', None)

        if latitude and longitude:
            """Provide distance between coordinates(lat, lng) and location of users"""
            pnt = GEOSGeometry(f"POINT({latitude} {longitude})", srid=4326)
            qs = qs.annotate(distance=Distance('location', pnt, spheroid=True)).order_by('distance')
            return qs

        # if not coords than shows distance from current user to others
        qs = qs.annotate(distance=Distance('location', self.request.user.location, spheroid=True)).order_by('distance')
        return qs



























