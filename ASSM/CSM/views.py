from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .serializers import AuthorregistrationSerializer, AuthorLoginSerializer, AuthorProfileSerializer, AuthorChangepasswordSerializer, SendPasswordResetEmailSerializer, AuthorPasswordresetSerializer
from django.contrib.auth import authenticate
from CSM.Renderers import AuthorRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from CSM.models import Author

# Creating User view.

# Generate Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class AuthorregistrationView(APIView):
    renderer_classes = [AuthorRenderer]
    def post(self, request, format=None):
        serial = AuthorregistrationSerializer(data=request.data)
        if serial.is_valid(raise_exception=True):
            user = serial.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'Registered Successful'},status=status.HTTP_201_CREATED)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthorLoginView(APIView):
    renderer_classes = [AuthorRenderer]
    def post(self, request, format=None):
        serial = AuthorLoginSerializer(data=request.data)
        if serial.is_valid(raise_exception=True):
            email = serial.data.get('email')
            password = serial.data.get('password')
            user_data = authenticate(email=email, password=password)
            if user_data is not None:
               token = get_tokens_for_user(user_data)
               return Response({'token': token, 'msg':'Login sucessful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'Enter_fields':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Authorprofile(APIView):
    renderer_classes=[AuthorRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = Author.objects.all()
        serializer = AuthorProfileSerializer(user, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)
    

class AuthorChangePasswordView(APIView):
    renderer_classes=[AuthorRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = AuthorChangepasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed sucessful'}, status=status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
  renderer_classes = [AuthorRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class AuthorpasswordResetView(APIView):
    renderer_classes = [AuthorRenderer]
    def post(self, request, uid, token, format = None):
        serializer = AuthorPasswordresetSerializer(data=request.data,
        context={'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password updated sucessfully'}, status=status.HTTP_200_OK)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)