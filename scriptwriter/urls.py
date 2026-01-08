from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'scriptwriter'

# REST API Router
router = DefaultRouter()
router.register(r'characters', views.CharacterViewSet, basename='character')
router.register(r'scripts', views.ScriptViewSet, basename='script')
router.register(r'versions', views.ScriptVersionViewSet, basename='version')
router.register(r'scenes', views.SceneViewSet, basename='scene')
router.register(r'jobs', views.JobViewSet, basename='job')

urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    
    # REST API endpoints
    path('api/', include(router.urls)),
    path('api/jobs/create/', views.create_job, name='create_job'),
    path('api/jobs/<str:job_id>/status/', views.job_status, name='job_status'),
    path('api/jobs/<str:job_id>/result/', views.job_result, name='job_result'),
    
    # Legacy endpoints (for backwards compatibility)
    path('api/generate/', views.generate_script, name='generate_script'),
    path('api/save/', views.save_script, name='save_script'),
]

