from django.contrib import admin
from .models import Image
# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    #admin페이지에 어떤 column을 관리할지 설정이 가능함
    #list_display 관리자페이지에서 볼거 작성
    #list_display = ['idx', 'email', 'image']
    list_display = ['id','email', 'image']

admin.site.register(Image, ImageAdmin)
#site에 등록


