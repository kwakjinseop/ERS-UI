from django.db import models
# Create your models here.
# DB에 저장하기 위한 모델...
# 이름, 이메일, 비밀번호
# DB 관련 수정사항 생기면 마이그레이션 다시 해야함~~~!!!!!1
# https://infinitt.tistory.com/65?category=1072777 : DB 반영
# https://breadnbutter.tistory.com/4 : pk 설정 & 데이터 id 부분..암튼 그런거

class Account(models.Model):
    username = models.CharField(max_length=32, verbose_name='이름', default="")
    useremail = models.EmailField(max_length=128, unique=True, primary_key=True, verbose_name='이메일', default="")
    password = models.CharField(max_length=64, verbose_name='비밀번호', default="")

    #데이터가 문자열로 변환이 될 때 어떻게 나올지 정의하는 함수
    def __str__(self):
        return self.useremail

    class Meta:
        db_table = 'account'
        verbose_name = '사용자 계정'
        verbose_name_plural = '사용자 계정'
