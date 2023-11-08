from rest_framework import serializers
from .models import Technology, Experience

class TechnologySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Technology
        fields = '__all__'
     
class ExperienceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Experience
        fields = '__all__'   
        