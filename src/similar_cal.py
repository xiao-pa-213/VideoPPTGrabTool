import cv2
import numpy as np
from skimage.metrics import structural_similarity

# def is_similar_alg(img1, img2, threshold,alg=enumerate('ssim','hist','ncc','cos')):
#     if alg == "ssim":
#         is_similar_ssim(img1, img2, threshold)
#         return 1
#     elif alg == "hist":
#         is_similar_hist(img1, img2, threshold)
#         return 1
#     elif alg == "ncc":
#         is_similar_ncc(img1, img2, threshold)
#         return 1
#     elif alg == "cos":
#         is_similar_cos(img1, img2, threshold)
#         return 1
#     else:
#         return 0

#准度高 速度慢
def is_similar_ssim(img1, img2, threshold=0.9):
    # 将图像转换为灰度图像
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 计算SSIM指数
    ssim_value = structural_similarity(gray1, gray2)
    # 判断SSIM指数是否超过阈值
    return ssim_value > threshold

#准度速度适中
def is_similar_ncc(img1, img2, threshold=0.9):
    # Normalize the images to zero mean and unit variance
    img1 = img1 - np.mean(img1)
    img1 = img1 / np.std(img1)
    img2 = img2 - np.mean(img2)
    img2 = img2 / np.std(img2)

    # Calculate the cross correlation coefficient
    ncc_value = np.sum(img1 * img2) / np.sqrt(np.sum(img1 ** 2) * np.sum(img2 ** 2))

    return ncc_value > threshold

#准度差 较快
def is_similar_cos(img1, img2, threshold=0.9):
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    orb = cv2.ORB_create()
    kps1, descs1 = orb.detectAndCompute(gray1, None)
    kps2, descs2 = orb.detectAndCompute(gray2, None)

    dot_product = np.dot(descs1, descs2.T)
    norm_features1 = np.linalg.norm(descs1)
    norm_features2 = np.linalg.norm(descs2)
    cosine_sim = dot_product / (norm_features1 * norm_features2)
    average_cosine_sim = np.mean(cosine_sim)
    return average_cosine_sim > threshold

#准度差 较快
def is_similar_hist(img1,img2,threshold=0.9):
    hist1 = cv2.calcHist(img1, [0, 1, 2], None, [32, 32, 32], [0, 256, 0, 256, 0, 256])
    hist2 = cv2.calcHist(img2, [0, 1, 2], None, [32, 32, 32], [0, 256, 0, 256, 0, 256])
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return similarity > threshold

