from django.db import models
from account.models import Account
# 참고
# https://wikidocs.net/91424 : 이미지 업로드 관련
# https://eveningdev.tistory.com/47
# https://dheldh77.tistory.com/entry/Django-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%85%EB%A1%9C%EB%93%9C
# https://github.com/ForPT/ForPresenTation_Django : 경환선배 깃허브
# https://hashcode.co.kr/questions/9573/django-db-primary_key-%EC%82%AD%EC%A0%9C-%EC%A7%88%EB%AC%B8%EB%93%9C%EB%A6%BD%EB%8B%88%EB%8B%A4
# : id pk처리 관련 Q&A
# https://ssungkang.tistory.com/entry/Django-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-%EC%A1%B0%ED%9A%8C-queryset
# : db 조건문 관련

# Create your models here.
def file_name(instance, filename):
 #   return 'files/ppts/{}_{}_{}.png'.format(instance.email, instance.image)
    return 'images/{}_{}'.format(instance.email, instance.image)
    #이미지가 이미 .jpeg 아님 jpg인데 끝이 .png인게 맞나?! 그리고 중복 데이터 마지막 변하는건 같음


class Image(models.Model):
    #사용자 이메일, 파일명
    #null은 데이터베이스상에서 null값 허용, blank는 입력을 받을 때 없어도 된다고
    #엄연히 다르다고 하는데 차이를 잘 모르겠음
    #idx = models.CharField(default='', null=True, max_length=64)
    id = models.AutoField(primary_key=True),
    #email = models.EmailField(max_length=128, verbose_name='이메일', default="")
    email = models.CharField(max_length=128, verbose_name='이메일', default="")
    #근데 저장명에 @이가 보이지 않음...이게 맞음?? email이랑 charfiled 모두 같은 현상임
    #근데 골뱅이 없으면 조회를 어케하징
    #email = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account', db_column="account_useremail", verbose_name='이메일', blank=True, null=True)
    image = models.FileField(upload_to=file_name, verbose_name='이미지')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'image'
        verbose_name= '이미지업로드'
        verbose_name_plural= '이미지업로드'