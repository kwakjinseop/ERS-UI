from django.db import models

class Document(models.Model):
    # title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "Uploaded Files/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)

class Members(models.Model):
    useremail = models.EmailField(max_length=128, verbose_name='사용자 이메일')
    username = models.CharField(max_length=32, verbose_name='사용자 이름')
    password = models.CharField(max_length=64, verbose_name='사용자 비밀번호')




