from django.shortcuts import render
from rest_framework import viewsets
from .models import Software
from .serializers import SoftwareSerializer

class SoftwareViewSet(viewsets.ModelViewSet):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer

