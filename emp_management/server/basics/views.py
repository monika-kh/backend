from .models import Technology, Experience
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import ExperienceSerializer, TechnologySerializer


from rest_framework import generics

class TechnologyViewSet(generics.ListCreateAPIView):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Technology.objects.all()
        serializer = TechnologySerializer(queryset, many=True)
        return Response(serializer.data)
    
class ExperienceViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        queryset = Experience.objects.all()
        serializer = ExperienceSerializer(queryset, many=True)
        return Response(serializer.data)