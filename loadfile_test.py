import os
import cv2

# path_dir = 'media/Uploaded Files'
path_dir = 'media/Uploaded Files'
file_list = os.listdir(path_dir)
img_name = file_list[0]
print(img_name)


# file_list = os.listdir(path_dir)
# # print(file_list)
#
# # img_name = path_dir + '/' + file_list[0]
# # print(img_name)
#
#
#
# img_name = file_list[0]
# # font = cv2.FONT_HERSHEY_SIMPLEX
# file_name = input(img_name)  # 이미지 파일경로 입력 -> 수정필요!
# print(file_name)
# # img = cv2.imread(img_name, cv2.IMREAD_COLOR)
# # print(img)
# # cv2.imshow('image', img)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()