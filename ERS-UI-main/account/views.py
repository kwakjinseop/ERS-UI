from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from .models import Account
from django.contrib import messages

# Create your views here.
# 참고 사이트
# https://gosmcom.tistory.com/126 :회원가입 & 로그인
# https://hyongdoc.tistory.com/433 :회원가입 & 로그인
# https://infinitt.tistory.com/65?category=1072777 :회원가입 & 로그인
# https://gosmcom.tistory.com/141 :회원가입 & 로그인
# https://my-repo.tistory.com/38 : 중복체크
# https://galid1.tistory.com/299 : url에서 name 사용하기

#회원가입 함수
def register(request):
    #return render(request, 'signup.html')
    if request.method == 'GET':
        #페이지 불러올때
        return render(request, 'signup.html')

    elif request.method=='POST':
        #페이지 내에서 회원 등록하기 버튼을 눌렀을 시
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password',None)

        response = {} #응답 저장

        #항목에 공백있을 때
        if not(username and useremail and password and re_password):
            response['error']='모든 항목에 입력을 해주세요.'
            return render(request, 'signup.html', response)

        #이메일 중복 확인
        elif Account.objects.filter(useremail=useremail).exists():
            response['error'] = '이미 존재하는 이메일입니다.'
            return render(request, 'signup.html', response)

        #비번이랑 비번확인이랑 다를때
        elif password != re_password:
            #return HttpResponse("비밀번호가 다릅니다.")
            response['error']='비밀번호가 다릅니다.'
            return render(request, 'signup.html', response)
            #여기 부분은 나중에 html에서 error 부분에 코드 수정으로
            #페이지 이동 없이 예외처리

        #모든 항목에 충족하고 같으면 회원가입 저장~
        else:
            account = Account(
                username = username,
                useremail = useremail,
                password = make_password(password),
                #일치확인할때는 check_password이용
            )

            account.save()
            #return redirect('/account/login')
            return redirect(reverse('login'))
            #return render(request, 'login.html', response)

        #return render(request, 'signup.html', response)
        #login 페이지 불러내면 주소는 어케되나 /account/login으로 넘어가는지?

#로그인
def login(request):
    # return render(request, 'login.html')
    response1 = {}

    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        login_useremail = request.POST.get('useremail', None)
        login_password = request.POST.get('password', None)

        #칸에 모두 작성하지 않았을 때
        if not(login_useremail and login_password):
            response1['error'] = '이메일과 비밀번호를 모두 입력하세요.'
            #messages.info(request, '이메일과 비밀번호를 모두 입력하세요.')
            #기존의 error메시지와 다를게 없고 걍 부트스트랩 빨인듯 하다..
            return render(request, 'login.html', response1)

        #이메일 존재하지 않을 때
        elif not Account.objects.filter(useremail=login_useremail).exists():
            response1['error'] = '존재하지 않는 이메일입니다.'
            return render(request, 'login.html', response1)

        else:
            account = Account.objects.get(useremail=login_useremail)
            #db에서 꺼내는 명령, post로 받아온 username으로 db username을 꺼냄

            #아이디가 존재하고 비번도 일치할 때
            if check_password(login_password, account.password):
                #request.session['user'] = account.id
                request.session['user'] = account.useremail
                #세션 - 일정시간 웹브라우전를 통해 들어오는 정보를 하나의 상태로
                #보고 정보를 유지시키는 기술이다. 사용자 식별에 필요

                return redirect(reverse('index'))
                #return render(request, 'main.html', name)

            #비밀번호가 틀렸을 때
            else:
                response1['error']='비밀번호를 확인해주세요.'
                return render(request, 'login.html', response1)

        #return render(request, 'login.html', response1)

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))