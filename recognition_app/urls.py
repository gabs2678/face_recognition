from django.urls import path
from . import views

urlpatterns = [
    path('detect_faces/', views.upload_and_detect_image, name='detect_faces'),
]
