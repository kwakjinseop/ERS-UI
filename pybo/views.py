from django.shortcuts import render
from .models import Image, Template, Result
from django.http import HttpResponse
from django.db import models

from account.models import Account

import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import easyocr  # 이렇게 해야지 오류 없이 잘 돌아감 (https://jaeniworld.tistory.com/8)
import cv2
import numpy as np

reader = easyocr.Reader(['ko', 'en'], gpu=True)  # this needs to run only once to load the model into memory


# 참고
# https://gosmcom.tistory.com/143 : 로그인 처리 이름 불러오기
# https://free-eunb.tistory.com/43 : 이미지 for 문처리

# 템플릿테이블 가져오기
def templateMenu(request):
    template = Template.objects.all()
    # print("abcd")
    return render(request, 'templateMenu.html', {'templates': template})


# def useTemplate(request, pk):
#     # usetemplates = Template.objects\
#     print('views.py/useTemplate()/request: {request}')
#     print('views.py/useTemplate()/pk: ', pk)
#     gettemplate = Template.objects.get(pk=pk)
#
#     return render(request, 'useTemplate.html', {'gettemplates': gettemplate}, pk)

    # return render(request, 'useTemplate.html', {'usetemplate': usetemplates})


def usetemplate(request, pk):
    gettemplate = Template.objects.get(pk=pk)
    return render(request, 'useTemplate.html', {'gettemplate': gettemplate})


#그룹화하는 페이지로 넘어가는거
def makeGroup(request):
    results = Result.objects.all()
    return render(request, 'makeGroup.html', {'results': results})

#그룹화버튼 눌렀을때 작동하도록
def Group(request):
    global list
    if request.method == 'POST':
        selected_result = request.POST.getlist('selected_result')
        print("그룹화", selected_result)
        list = selected_result

    return render(request, 'makeGroup.html', list)


def pop(request):
    return render(request, 'pop.html')


def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.!")
    userstate = request.session.get('user')
    name = {}

    if userstate:  # 현재 로그인 상태이면! 이름을 출력할 수 있게끔
        account = Account.objects.get(pk=userstate)
        # name['name'] = '문진영'
        name['name'] = account.username

        return render(request, 'realmainpage.html', name)

    else:
        return render(request, 'realmainpage.html')


def use(request):
    userstate = request.session.get('user')
    account = Account.objects.get(pk=userstate)
    name = {}
    name['name'] = '메롱'

    if request.method == "POST":
        img = request.FILES.get('image', None)

        if not img:
            # 에러메시지 출력해줬음 좋겠음 이미지를 선택해주세요~~뭐 이런거 일단은 새로고침 형태로 이동
            return render(request, 'use.html', name)

        else:
            image = Image(
                # idx = request.session.get('user'),
                email=account.useremail,
                image=img,
            )

            image.save()

            # imgList = Image.objects.filter(email=account.useremail)
            # return HttpResponse(Image.image)

            img = cv2.imread(
                'C:\\Users\\hufs_ice\\PycharmProjects\\DoCatch\\ERS-UI\media\\images\\ko1naver.com_serial14-2.jpg')
            result = reader.readtext(
                'C:\\Users\\hufs_ice\\PycharmProjects\\DoCatch\\ERS-UI\media\\images\\ko1naver.com_serial14-2.jpg')
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
    return render(request, 'use.html', {'imgList': imgList})


def useTemplate(request):
    # userstate = request.session.get('user')
    # account = Account.objects.get(pk=userstate)
    # name = {}
    #
    # if request.method == "POST":
    #     img = request.FILES.get('image', None)
    #
    #     if not img:
    #         return render(request, 'useTemplate.html', name)
    #
    #     else:
    #         image = Image(
    #             email=account.useremail,
    #             image = img,
    #         )
    #
    #         image.save()
    #
    #         img = cv2.imread('C:\\Users\\hufs_ice\\PycharmProjects\\DoCatch\\ERS-UI\media\\images\\ko1naver.com_serial14-2.jpg')
    #         result = reader.readtext('C:\\Users\\hufs_ice\\PycharmProjects\\DoCatch\\ERS-UI\media\\images\\ko1naver.com_serial14-2.jpg')
    #         # 왼쪽위, 왼쪽아래, 오른쪽아래, 오른쪽위
    #         for i in range(len(result)):
    #             if i == 0:
    #                 print('[', result[i], ',')
    #             elif i == len(result) - 1:
    #                 print(result[i], ']')
    #             else:
    #                 print(result[i], ',')
    #         i = 0
    #         for (bbox, text, prob) in result:
    #             i += 1
    #             (tl, tr, br, bl) = bbox
    #             tl = (int(tl[0]), int(tl[1]))
    #             tr = (int(tr[0]), int(tr[1]))
    #             br = (int(br[0]), int(br[1]))
    #             bl = (int(bl[0]), int(bl[1]))
    #
    #             cv2.rectangle(img, tl, br, (0, 255, 0), 2)
    #         cv2.imshow("Image", img)
    #
    # imgList = Image.objects.filter(email=account.useremail)
    # return render(request, 'useTemplate.html', {'imgList':imgList})

    # 이렇게 하면 페이지 연결은 됨
    userstate = request.session.get('user')
    name = {}

    if userstate:  # 현재 로그인 상태이면! 이름을 출력할 수 있게끔
        account = Account.objects.get(pk=userstate)
        # name['name'] = '문진영'
        name['name'] = account.username

        return render(request, 'useTemplate.html', name)

    else:
        return render(request, 'useTemplate.html')


def maketemplate(request):
        return render(request, 'maketemplate.html')


def click(request):
    return


def ocr(request):
    font = cv2.FONT_HERSHEY_SIMPLEX
    file_name = input("분석할 파일명을 입력해주세요: ")  # 이미지 파일경로 입력 -> 수정필요!
    file_path = f'C:/Users/kyung/Downloads/{file_name}'  # 이미지경로
    img_array = np.fromfile(file_path, np.uint8)  # 이미지를 배열로 변환
    print('You want to see: ', file_path)  # 확인용
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 배열을 이미지로 변환
    result = reader.readtext(img)  # 이미지에서 택스트 추출

    # 왼쪽위, 왼쪽아래, 오른쪽아래, 오른쪽위
    # 결과(results) 출력 용
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
        print('BBox-size:', height * weight)
        print('Confidence Score:', round(result[0][2], 2), end='\n')
    idx = 0
    for (bbox, text, prob) in result:
        idx += 1
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        img = cv2.rectangle(img, tl, br, (0, 0, 255), 2)  # bbox그리기
        img = cv2.putText(img, str(idx), tl, font, 1, (0, 0, 255), 2)  # idx번호 표시하기
    # bbox와 idx를 그린 이미지(img)는 변수에만 저장되어 있고 DB에는 반영되지 않았다. 
    # imwrite를 통해 로컬에 이미지 저장을 할 수 있지만 DB에 저장하기 위해선 어떻게 해야할지?
    cv2.imshow("Image", img)  # 이미지 보여주기, 아직 저장하진 않음
    cv2.waitKey(0)  # imshow와 짝꿍


# 진섭이꺼에서 합침
def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data

        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(

            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "../templates/maketemplate.html", context = {
        "files": documents
    })

def Homepage(request):

    return render(request, 'homepage.html')