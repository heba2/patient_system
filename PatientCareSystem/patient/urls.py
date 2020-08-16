from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('patients', views.PatientVs, basename='patients')
router.register('profiles', views.ProfileVs, basename='profiles')
router.register('appointments', views.AppointmentVs, basename='appointments')
router.register('appointments', views.AppointmentVs, basename='appointments')
router.register('users', views.UserVs, basename='users')


app_name = 'patient'
urlpatterns = [


]

urlpatterns = urlpatterns + router.urls
