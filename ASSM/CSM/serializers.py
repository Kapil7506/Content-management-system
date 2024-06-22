from xml.dom import ValidationErr
from rest_framework import serializers
from CSM.models import Author
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from CSM.utils import Util
from django.core.mail import send_mail
class AuthorregistrationSerializer(serializers.ModelSerializer):
    #confirming password
    phone_no = serializers.CharField()
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Author
        fields = ['email', 'First_name', 'Last_name', 'phone_no', 'pincode', 'password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

#Validate password

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
          raise serializers.ValidationError("Please enter same password")
        return attrs

    def create(self, validate_data):
        return Author.objects.create_user(**validate_data)
    
class AuthorLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = Author
        fields = ['email', 'password']


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'email', 'First_name', 'Last_name', 'phone_no', 'pincode']

class AuthorChangepasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password2'}, write_only = True)
    class Meta:
        fields =['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)
        user = self.context.get('user')
        if password != password2:
          raise serializers.ValidationError("Please enter same password")
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    class Meta:
        fields  =['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if Author.objects.filter(email=email).exists():
           user = Author.objects.get(email = email) 
           uid = urlsafe_base64_encode(force_bytes(user.id))
           print('Encoded UID' , uid)
           token = PasswordResetTokenGenerator().make_token(user)
           print('Password Reset Token', token)
           link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
           print('Password Reset Link', link)
           #send Email
           body = 'Click Following Link to Reset Paasword '+link
           data = {
               'subject': 'Reset password',
               'body': body,
               'to_email': user.email
           }
           Util.send_email(data)
           return attrs
        else:
            raise serializers.ValidationError('You are not Registered')
        

class AuthorPasswordresetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password2'}, write_only = True)
    class Meta:
        fields =['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.pop('password2', None)
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
              raise serializers.ValidationError("Please enter same password")
            id = smart_str(urlsafe_base64_decode(uid))
            user= Author.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or expired')
            user.set_password(password)
            user.save()

            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Toeken is not valid or Expired')