# import cv2
# import numpy as np


# from PIL import Image, ImageFilter

# # 打开图像
# image = Image.open("C:/Users/三三sama/Desktop/R-C-pro.jpg")

# # 使用锐化滤波器进行边缘增强
# enhanced = image.filter(ImageFilter.SHARPEN)

# # 显示原图和增强后的图像
# image.show()
# enhanced.show()

import cv2 as cv
import numpy as np

img = cv.imread("D:/baidu_download/chat/R-C-pro.jpg")
h = img.shape[0]
w = img.shape[1]

# 均值滤波
img_Blur_3 = cv.blur(img, (2, 2))  # 3*3均值滤波


# 中值滤波
img_MedianBlur_3 = cv.medianBlur(img, 3)  # 3*3中值滤波


# # 超限像素平滑法
# def overrun_pixel_smoothing(kernel, image):
#     img_overrun = image.copy()
#     filter = np.zeros((kernel, kernel), np.uint8)
#     average = np.zeros((h - kernel + 1, w - kernel + 1), np.uint8)  # 平均值矩阵

#     for i in range(h - kernel + 1):
#         for j in range(w - kernel + 1):

#             for m in range(kernel):
#                 for n in range(kernel):
#                     filter[m, n] = img_overrun[i + m, j + n]

#             average[i, j] = 1 / (kernel * kernel) * filter.sum()  # 求平均

#     T = 50  # 设定阈值

#     for i in range(h - kernel + 1):
#         for j in range(w - kernel + 1):

#             if abs(img[i + kernel - 2, j + kernel - 2] - average[i, j]) > T:
#                 img_overrun[i + kernel - 2, j + kernel - 2] = average[i, j]

#     return img_overrun


# img_overrun_3 = overrun_pixel_smoothing(3, img)  # 核大小为3*3

# # 有选择保边缘平滑法
# img_EdgeKeeping = img.copy()

# filter = np.zeros((5, 5), np.uint8)

# for i in range(h - 4):
#     for j in range(w - 4):

#         for m in range(5):
#             for n in range(5):
#                 filter[m, n] = img_EdgeKeeping[i + m, j + n]

#         mask = []

#         # 3*3掩膜
#         mask.append(
#             [
#                 filter[1, 1],
#                 filter[1, 2],
#                 filter[1, 3],
#                 filter[2, 1],
#                 filter[2, 2],
#                 filter[2, 3],
#                 filter[3, 1],
#                 filter[3, 2],
#                 filter[3, 3],
#             ]
#         )

#         # 5*5掩膜
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[1, 1],
#                 filter[1, 2],
#                 filter[1, 3],
#                 filter[0, 1],
#                 filter[0, 2],
#                 filter[0, 3],
#             ]
#         )
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[1, 1],
#                 filter[2, 1],
#                 filter[3, 1],
#                 filter[1, 0],
#                 filter[2, 0],
#                 filter[3, 0],
#             ]
#         )
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[3, 1],
#                 filter[3, 2],
#                 filter[3, 3],
#                 filter[4, 1],
#                 filter[4, 2],
#                 filter[4, 3],
#             ]
#         )
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[1, 3],
#                 filter[2, 3],
#                 filter[3, 3],
#                 filter[1, 4],
#                 filter[2, 4],
#                 filter[3, 4],
#             ]
#         )

#         # 6*6掩膜
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[3, 2],
#                 filter[2, 3],
#                 filter[3, 3],
#                 filter[4, 3],
#                 filter[3, 4],
#                 filter[4, 4],
#             ]
#         )
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[2, 3],
#                 filter[1, 2],
#                 filter[1, 3],
#                 filter[1, 4],
#                 filter[0, 3],
#                 filter[0, 4],
#             ]
#         )
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[1, 2],
#                 filter[2, 1],
#                 filter[1, 1],
#                 filter[0, 1],
#                 filter[1, 0],
#                 filter[0, 0],
#             ]
#         )
#         mask.append(
#             [
#                 filter[2, 2],
#                 filter[2, 1],
#                 filter[3, 2],
#                 filter[3, 1],
#                 filter[3, 0],
#                 filter[4, 1],
#                 filter[4, 0],
#             ]
#         )

#         # 求各掩膜的方差
#         var = []
#         for k in range(9):
#             var.append(np.var(mask[k]))

#         index = var.index(min(var))  # 方差最小的掩膜对应的索引号
#         img_EdgeKeeping[i + 2, j + 2] = np.mean(mask[index])


# cv.imshow("image", img)
# cv.imshow("img_Blur_3", img_Blur_3)
cv.imwrite("D:/baidu_download/chat/R-C-pro-mix.jpg", img_Blur_3)
# cv.imshow("img_MedianBlur_3", img_MedianBlur_3)

# cv.imshow("img_overrun_3", img_overrun_3)

# cv.imshow("img_EdgeKeeping", img_EdgeKeeping)

cv.waitKey(0)
cv.destroyAllWindows()
