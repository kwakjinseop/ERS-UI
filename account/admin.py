from django.contrib import admin
from .models import Account
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    #admin페이지에 어떤 column을 관리할지 설정이 가능함
    #list_display 관리자페이지에서 볼거 작성
    list_display = ('username', 'useremail', 'password')


admin.site.register(Account, UserAdmin)
#site에 등록