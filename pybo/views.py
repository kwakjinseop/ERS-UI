
from django.shortcuts import render
from .models import Image
from django.http import HttpResponse

from account.models import Account

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import easyocr # 이렇게 해야지 오류 없이 잘 돌아감 (https://jaeniworld.tistory.com/8)
import cv2
print('Success import easyocr and cv2!')
import numpy as np
reader = easyocr.Reader(['ko', 'en'], gpu=False) # this needs to run only once to load the model into memory

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

            img = cv2.imread('C:\\Users\\hufs_ice\\PycharmProjects\\DoCatch\\ERS-UI\media\\images\\ko1naver.com_serial14-2.jpg')
            result = reader.readtext('C:\\Users\\hufs_ice\\PycharmProjects\\DoCatch\\ERS-UI\media\\images\\ko1naver.com_serial14-2.jpg')
            # 왼쪽위, 왼쪽아래, 오른쪽아래, 오른쪽위
            for i in range(len(result)):
                if i == 0:
                    print('[', result[i], ',')
                elif i == len(result) - 1:
                    print(result[i], ']')
                else:
                    print(result[i], ',')
            i = 0
            for (bbox, text, prob) in result:
                i += 1
                (tl, tr, br, bl) = bbox
                tl = (int(tl[0]), int(tl[1]))
                tr = (int(tr[0]), int(tr[1]))
                br = (int(br[0]), int(br[1]))
                bl = (int(bl[0]), int(bl[1]))

                cv2.rectangle(img, tl, br, (0, 255, 0), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(0)

    imgList = Image.objects.filter(email=account.useremail)
    return render(request, 'use.html', {'imgList':imgList})


def click(request):

    return

# EasyOCR을 통해 특정경로에 있는 이미지에 접근해서 해당이미지위에 bbox를 표시해주는 함수
def ocr(request):
    file_name = input("분석할 파일명을 입력해주세요: ") # 분석할 파일경로 입력 -> 수정필요
    
    file_path = f'C:/Users/kyung/Downloads/{file_name}' # 분석할 파일경로 입력
    img_array = np.fromfile(file_path, np.uint8) # 이미지를 배열형태로 변환
    print('You want to see: ', file_path) # 확인용
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR) # 배열 decode하기
    result = reader.readtext(img) # 텍스트 추출하기

    # 왼쪽위, 왼쪽아래, 오른쪽아래, 오른쪽위
    for i in range(len(result)):
        if i == 0:
            print('[', result[i], ',')
        elif i == len(result) - 1:
            print(result[i], ']')
        else:
            print(result[i], ',')
    # ([[0, 5], [327, 5], [327, 114], [0, 114]], '1 1 00 /', 0.9260980801041065)
    if len(result) != 0:
        text = ''.join(result[0][1].split())
        print('\nTitle-Text:', text)
        print('Top-left:', result[0][0][0])
        print('Btm-left:', result[0][0][1])
        print('Btm-right:', result[0][0][2])
        print('Top-right:', result[0][0][3])
        height = result[0][0][1][0] - result[0][0][0][0]
        weight = result[0][0][2][1] - result[0][0][1][1]
        print('BBox-size:', height*weight)
        print('Confidence Score:', round(result[0][2], 2), end='\n')
    idx = 0
    for (bbox, text, prob) in result:
        idx += 1
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))


        img = cv2.rectangle(img, tl, br, (0, 0, 255), 2)
        img = cv2.putText(img, str(idx), tl, font, 1, (0, 0, 255), 2)
    # 현재로썬 이미지에 bbox가 그려진 이미지(img)는 변수에만 저장되어 있다 이를 imwrite함수를 통해 로컬에서 저장할 수 있었다.
    # DB에 저장할 땐 어떻개 해야할 것인가?
    cv2.imshow("Image", img) # img 보여주기 기능, 저장하진 않음
    cv2.waitKey(0)
