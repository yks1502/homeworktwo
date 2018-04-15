from promises.models import Promise
from promises.serializers import PromiseSerializer, PromiseUpdateSerializer, UserSerializer, UserAllSerializer
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from promises.permissions import IsOwner
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class PromiseList(generics.ListCreateAPIView):
  queryset = Promise.objects.all()
  serializer_class = PromiseSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

  def perform_create(self, serializer):
    serializer.save(user1=self.request.user)

class PromiseDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Promise.objects.all()
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner,)

  def get_serializer_class(self):
    if self.request.method in ['PUT', 'PATCH']:
      return PromiseUpdateSerializer
    return PromiseSerializer

class UserList(generics.ListCreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserAllList(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserAllSerializer

class UserAllDetail(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserAllSerializer

class CustomAuthLogin(ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    serializer = self.serializer_class(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({
      'token': token.key,
      'username': user.username,
      'id': user.id
    })