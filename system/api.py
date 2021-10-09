from system.models import *
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from knox.models import AuthToken
from system.serializer import UserSerializer, LoginSerializer


class loginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class =LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1],

        })
    