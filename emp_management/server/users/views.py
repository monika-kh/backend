from tokenize import TokenError
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = RegisterSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.type,
            'user_id': user.id,
            'employee_id': user.employee.all()[0].id
        })
        
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except TokenError:
                return Response({'detail': 'Invalid token.'}, status=400)
            return Response({'detail': 'Logout successful.'})
        else:
            return Response({'detail': 'No refresh token provided.'}, status=400)
