from django.shortcuts import render
from .models import Image
from django.http import HttpResponse

from account.models import Account

# 참고
# https://gosmcom.tistory.com/143 : 로그인 처리 이름 불러오기
# https://free-eunb.tistory.com/43 : 이미지 for 문처리

def index(request):
    #return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.!")
    userstate = request.session.get('user')
    name = {}

    if userstate: #현재 로그인 상태이면! 이름을 출력할 수 있게끔
        account = Account.objects.get(pk=userstate)
        #name['name'] = '문진영'
        name['name'] = account.username

        return render(request, 'main.html', name)

    else:
        return render(request, 'main.html')

def use(request):
    userstate = request.session.get('user')
    account = Account.objects.get(pk=userstate)
    name = {}
    name['name'] = '메롱'

    if request.method == "POST":
        img = request.FILES.get('image', None)

        if not img:
            #에러메시지 출력해줬음 좋겠음 이미지를 선택해주세요~~뭐 이런거 일단은 새로고침 형태로 이동
            return render(request, 'use.html', name)

        else:
            image = Image(
                #idx = request.session.get('user'),
                email=account.useremail,
                image = img,
            )

            image.save()

            #imgList = Image.objects.filter(email=account.useremail)
            #return HttpResponse(Image.image)
    imgList = Image.objects.filter(email=account.useremail)
    return render(request, 'use.html', {'imgList':imgList})


def click(request):

    return