from django.urls import path
from . import views

app_name = 'scriptwriter'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/generate/', views.generate_script, name='generate_script'),
    path('api/save/', views.save_script, name='save_script'),
]
