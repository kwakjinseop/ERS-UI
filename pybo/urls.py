from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('use/', views.use, name='use'),
    #path('use/', views.click),
]