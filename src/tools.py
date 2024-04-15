import os, cv2
import fnmatch
import numpy as np
from config import *

#检查路径是否存在，创建文件夹
def check_path(path):
    #找不到路径时创建路径
    if not os.path.exists(path):
        os.makedirs(path)

#清理文件夹内的png
def clean_images_in_path(path):
    imgset = []
    file_pattern = '*.png'

    #找不到路径时创建路径
    check_path(path)

    for filename in os.listdir(path):
        # 使用fnmatch.fnmatch()函数检查文件名是否与给定的模式匹配
        if fnmatch.fnmatch(filename, file_pattern):
            # 如果文件名匹配，打开文件并执行所需操作
            file_path = os.path.join(path, filename)
            # 在这里执行你想要的操作
            os.remove(file_path)
    print(f"已清空路径 {path} 下的图片")

#保存png到文件夹
def save_images2path(images, folder_path):
    for index, image in enumerate(images):
        file_name = f'frame_{index}.png'
        file_path = os.path.join(folder_path, file_name)
        cv2.imwrite(file_path, image)

#纯黑白判定
def is_almost_white_black_color(image):
    # 将图像转换为灰度格式
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 计算图像的均值和标准差
    mean = np.mean(gray_image)
    std = np.std(gray_image)

    # 白色阈值（可以调整）
    white_threshold_mean = 230
    white_threshold_std = 10
    # 黑色阈值（可以调整）
    black_threshold_mean = 10
    black_threshold_std = 10

    # 检查是否接近白色或黑色
    if (mean > white_threshold_mean and std < white_threshold_std) or \
            (mean < black_threshold_mean and std < black_threshold_std):
        return True
    else:
        return False

#模板匹配
def check_template(current_image, template_folder, threshold=0.8):
    templates = []

    # 读取模板库中的所有模板
    for filename in os.listdir(template_folder):
        template_path = os.path.join(template_folder, filename)
        template = cv2.imread(template_path)
        template_gray = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
        templates.append(template_gray)

    # 将当前图像转换为灰度图像
    gray_current_image = cv2.cvtColor(current_image, cv2.COLOR_BGR2GRAY)

    # 对于每个模板，计算与当前图像的匹配程度
    for template in templates:
        # 计算匹配程度
        result = cv2.matchTemplate(gray_current_image, template, cv2.TM_CCOEFF_NORMED)
        _, max_value, _, max_location = cv2.minMaxLoc(result)

        # 根据最大值确定当前图像是否包含模板
        if max_value > threshold:
            # print(f"当前图像包含模板：{filename}")
            return True

    # print("当前图像不包含任何模板")
    return False

