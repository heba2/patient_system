from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from .managers import CustomUserManager
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone_number'), max_length=20)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff'), default=True)
    is_active = models.BooleanField(_('active'), default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


Gender = (('Female', 'Female'),
          ('Male', 'Male'))


class Patient(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=25, blank=True)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(choices=Gender, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    patient_code = models.CharField(max_length=10, blank=True, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.name


def create_profile(sender, **kwarg):
    if kwarg['created']:
        Profile.objects.create(patient=kwarg['instance'])


post_save.connect(create_profile, sender=Patient)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name="patient", on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    appointment_type = models.CharField(choices=(('Examination', 'Examination'), ('Consultation', 'Consultation')),
                                        max_length=50)
    active = models.BooleanField(default=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return self.patient.name


class Assistant(models.Model):
    pass


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
