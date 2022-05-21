from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('use/', views.use, name='use'),
    path('maketemplate/', views.maketemplate, name='maketemplate'),
    path('<int:pk>/usetemplate/', views.usetemplate, name='usetemplate'),
    path('templateMenu/', views.templateMenu, name='templateMenu'),
    path('makeGroup/', views.makeGroup, name='makeGroup'),
    path('Group/', views.Group, name='Group'),
    path('pop/', views.pop, name='pop'),
    # 진섭이꺼 합친거임
    # path("", views.uploadFile, name = "uploadFile"),
    path("uploadFile", views.uploadFile, name="uploadFile"),
    path('ocr/', views.ocr, name="ocr"),
    path('home/', views.Homepage, name="Homepage"),

    # path('use/', views.click),
]
