from rest_framework import serializers
from .models import Patient, Profile, Appointment, Assistant, CustomUser

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()

    class Meta:
        model = Profile
        fields = '__all__'


class AssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assistant
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password2 != password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    @api_view(['POST'])
    @permission_classes([AllowAny])
    @ensure_csrf_cookie
    def login_view(self, request):
        User = CustomUser()
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email and password required')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        serialized_user = RegistrationSerializer(user).data

        token = Token.object.get(serialized_user=serialized_user)

        response.data = {
            'access_token': token,
            'user': serialized_user,
        }

        return response
