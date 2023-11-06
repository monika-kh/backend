from django.urls import path
from .views import TechnologyViewSet, ExperienceViewSet


urlpatterns = [
    path('tech_list', TechnologyViewSet.as_view(), name='tech'),
    path('exp_list', ExperienceViewSet.as_view({'get': 'list'}), name='exp')
]