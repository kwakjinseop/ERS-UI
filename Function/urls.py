from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "Function"

urlpatterns = [
    path("", views.uploadFile, name = "uploadFile"),
    path('ocr/', views.ocr, name="ocr"),
    path('home/', views.Homepage, name="Homepage"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )