from rest_framework.generics import CreateAPIView, DestroyAPIView
from .serializers import RegistrationSerializer, ActivationSerializer, LoginSerializer, ChangePasswordSerializer, DropPasswordSerializer, ChangeForgottenPassword
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class RegistrationView(CreateAPIView):
    serializer_class=RegistrationSerializer


class ActivationView(CreateAPIView):
    serializer_class = ActivationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response(
            {'message': 'Аккаунт успешно активирован'},
            status=status.HTTP_202_ACCEPTED      
            )
    
class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

class LogoutView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Token.objects.get(user=request.user).delete()
        return Response(
            {'message': 'Logged Out'},
            status=status.HTTP_204_NO_CONTENT
        )
    

class ChangePasswordView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response({'message': 'Пароль успешно обновлен'}, status=status.HTTP_200_OK)
    

class DropPasswordView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = DropPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_activation_code()
        return Response({'message': 'Activation code sended'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ChangeForgottenPasswordView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        serializer = ChangeForgottenPassword(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response({'message': 'Password changed succesfuly'}, status=status.HTTP_201_CREATED)
    
    

    