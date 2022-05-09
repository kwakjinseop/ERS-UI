from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('use/', views.use, name='use'),
    path('template/', views.template, name='template')
    #path('use/', views.click),
]