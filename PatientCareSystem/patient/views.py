from .serializers import ProfileSerializer, PatientSerializer, AppointmentSerializer, RegistrationSerializer
from rest_framework import viewsets
from .models import Profile, Patient, Appointment
from.models import CustomUser


class PatientVs(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class AppointmentVs(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class ProfileVs(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserVs(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
