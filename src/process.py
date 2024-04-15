import os, cv2, re, shutil, math
from config import *
from similar_cal import *
from tools import *
from tqdm import tqdm

#读取视频中一N间隔的帧
def read_video_frames(video_path, n_seconds, local_save = False, save_path = ''):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("无法打开视频文件。是否已将视频拖入文件夹或配置好config.py文件？")
        return 0
    fps = video.get(cv2.CAP_PROP_FPS)
    total_duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    num_frames = int(total_duration / n_seconds)
    print(f'视频长度为{round(total_duration,2)}秒 ({round(total_duration/3600,2)} hours)')

    #获取帧
    for i in tqdm(range(num_frames),desc=f"正在以{n_seconds}秒间隔提取帧",unit_scale=False):
        video.set(cv2.CAP_PROP_POS_FRAMES, i * n_seconds * fps)
        ret, frame = video.read()
        if not ret:
            break
        if local_save:
            index =video.get(cv2.CAP_PROP_POS_FRAMES)
            timestamp = round(video.get(cv2.CAP_PROP_POS_MSEC), 3)
            seconds = timestamp / 1000

            # 计算小时、分钟和秒
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            seconds = int(seconds % 60)
            # 格式化输出
            timestamp_format = f"{hours:02d}-{minutes:02d}-{seconds:02d}"
            cv2.imwrite(f'{save_path}/frame_{index}_{timestamp_format}.png', frame)

    video.release()
    return 1

#删除相邻的相似帧
def remove_similar_neibor_frames(threshold=0.9, read_path=''):
    #读取所有路径并排序
    image_paths = [os.path.join(read_path, f) for f in os.listdir(read_path) if f.endswith('.png')]
    image_paths.sort(
        key=lambda x: int(re.search(r'frame_(\d+)', x).group(1)) if re.search(r'frame_(\d+)', x) else 0)

    #比较算法
    unique_frames.append(cv2.imread(image_paths[0]))

    index = 0
    timestamp = re.search(r"_([0-9]{2}-[0-9]{2}-[0-9]{2})\.", unique_frames[-1]).group(1)
    file_name = f'frame_{index}_{timestamp}.png'
    file_path = os.path.join(output_picture_path, file_name)
    cv2.imwrite(file_path, unique_frames[-1])

    for path in tqdm(image_paths,desc="正在删除相邻相似帧",unit_scale=False):
        img = cv2.imread(path)
        if not is_similar_ssim(img, unique_frames[-1],threshold=0.9):
            unique_frames.append(img)

            index+=1
            timestamp = re.search(r"_([0-9]{2}-[0-9]{2}-[0-9]{2})\.", path).group(1)
            file_name = f'frame_{index}_{timestamp}.png'
            file_path = os.path.join(output_picture_path, file_name)
            cv2.imwrite(file_path, img)

    return 1

#提取所有连续子串
def pick_stable_frames(threshold=0.9,read_path='', SimilarCount=2):
    #SimilarCount    会被识别为重复子串的最小长度

    #读取所有路径并排序
    image_paths = [os.path.join(read_path, f) for f in os.listdir(read_path) if f.endswith('.png')]
    image_paths.sort(key=lambda x: int(re.search(r'frame_(\d+)', x).group(1)) if re.search(r'frame_(\d+)', x) else 0)

    #查找重复子串算法
    current_frame_start = cv2.imread(image_paths[0])# 重复子串中的首个元素
    current_frame_start_index = 0
    # 查找重复子串并记录首个元素
    progressbar = tqdm(total=len(image_paths),desc="正在提取主要静止帧",unit_scale=False)
    for i in range(1, len(image_paths)):
        img = cv2.imread(image_paths[i])
        if is_similar_ssim(img, current_frame_start, threshold):  # 比较是否相似
            progressbar.update(1)
            continue
        else:
            similar_frames_len = i - current_frame_start_index
            if similar_frames_len >= SimilarCount:
                #保存图片
                index = re.search(r'frame_(\d+)', image_paths[current_frame_start_index]).group(1)
                timestamp = re.search(r"_([0-9]{2}-[0-9]{2}-[0-9]{2})\.", image_paths[current_frame_start_index]).group(1)
                file_name = f'frame_{index}_{timestamp}.png'
                file_path = os.path.join(output_picture_path, file_name)
                cv2.imwrite(file_path, current_frame_start)
            current_frame_start_index = i
            current_frame_start = img
            progressbar.update(1)
    # 添加最后一个子串
    similar_frames_len = len(image_paths) - current_frame_start_index
    if similar_frames_len >= SimilarCount:
        # 保存图片
        index = re.search(r'frame_(\d+)', image_paths[current_frame_start_index]).group(1)
        timestamp = re.search(r"_([0-9]{2}-[0-9]{2}-[0-9]{2})\.", image_paths[current_frame_start_index]).group(1)
        file_name = f'frame_{index}_{timestamp}.png'
        file_path = os.path.join(output_picture_path, file_name)
        cv2.imwrite(file_path, current_frame_start)
    progressbar.update(1)
    progressbar.close()
    return 1

#去除无用帧
def remove_useless_frames(read_path=''):
    # 读取所有图片的路径并排序
    image_paths = [os.path.join(read_path, f) for f in os.listdir(read_path) if f.endswith('.png')]
    image_paths.sort(
        key=lambda x: int(re.search(r'frame_(\d+)', x).group(1)) if re.search(r'frame_(\d+)', x) else 0)

    # 判断每张图片是否有用
    progressbar = tqdm(total=len(image_paths),desc="正在去除无用画面",unit_scale=False)
    for i in range(0, len(image_paths)):
        img = cv2.imread(image_paths[i])

        # 模板匹配
        if check_template(img,template_path,threshold=0.6):
            source_image_path = image_paths[i]
            destination_folder_path = os.path.join(output_picture_path,"crashbin_auto")

            # 确保目标文件夹存在
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)
            shutil.move(source_image_path, destination_folder_path)

        # 判断纯色
        if is_almost_white_black_color(img):
            source_image_path = image_paths[i]
            destination_folder_path = os.path.join(output_picture_path, "crashbin_auto")

            # 确保目标文件夹存在
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)
            shutil.move(source_image_path, destination_folder_path)
        progressbar.update(1)
    progressbar.close()
    return 1

#去除重复帧
def remove_repeat_frames(read_path=''):
    # 读取所有图片的路径并排序
    image_paths = [os.path.join(read_path, f) for f in os.listdir(read_path) if f.endswith('.png')]
    image_paths.sort(
        key=lambda x: int(re.search(r'frame_(\d+)', x).group(1)) if re.search(r'frame_(\d+)', x) else 0)

    images = []
    for image_path in image_paths:
        images.append(cv2.imread(image_path))

    # 判断每张图片是否重复
    total_times = math.comb(len(image_paths),2)
    progressbar = tqdm(total=total_times,desc="正在去除重复画面",unit_scale=False)
    i=0
    while i < len(image_paths):
        img1 = images[i]
        j = i+1
        while j < len(image_paths):
            img2 = images[j]
            if is_similar_ncc(img1,img2,threshold=0.9):
                #移除img2
                source_image_path = image_paths[j]
                destination_folder_path = os.path.join(output_picture_path, "crashbin_auto")
                if not os.path.exists(destination_folder_path):
                    os.makedirs(destination_folder_path)
                shutil.move(source_image_path, destination_folder_path)

                #清理image_paths[]
                del image_paths[j]
                del images[j]
                total_times -= (len(image_paths) + 1)
                progressbar.total = total_times
            else:
                j+=1
            progressbar.update(1)
        i+=1
    progressbar.close()
    return 1
