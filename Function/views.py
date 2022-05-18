from django.shortcuts import render
from .import models
import easyocr
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True' #이거 넣어줘야 오류 안뜸
import cv2
import numpy as np
reader = easyocr.Reader(['ko', 'en'], gpu=True) # this needs to run only once to load the model into memory

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

def ocr(request):
    path_dir = 'media/Uploaded Files'
    file_list = os.listdir(path_dir)
    img_name = file_list[0]
    font = cv2.FONT_HERSHEY_SIMPLEX
    file_name = img_name  # 이미지 파일경로 입력 -> 수정필요!
    file_path = f'C:/Users/xmcdk/Desktop/ICE_Docatch/media/Uploaded Files/{file_name}'  # 이미지경로'  # 이미지경로
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

