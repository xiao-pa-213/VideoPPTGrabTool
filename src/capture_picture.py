import os
from config import *
from process import *
from tools import *

def check_read_video_frames():
    clean_images_in_path(pictemp_path)  # 清空pictemp文件夹
    if not read_video_frames(raw_video_path, n_seconds=garb_interval_n_seconds,
                             local_save=True, save_path=pictemp_path):  # 读取视频
        return 0
    return 1
def check_pick_stable_frames():
    clean_images_in_path(os.path.join(output_picture_path, "crashbin_manual"))  # 清空临时回收站
    clean_images_in_path(os.path.join(output_picture_path, "crashbin_auto"))  # 清空临时回收站
    clean_images_in_path(output_picture_path)  # 清空output_picture文件夹
    # remove_similar_neibor_frames(read_path=pictemp_path)
    pick_stable_frames(read_path=pictemp_path, threshold=0.95)

def remove_frames():
    remove_useless_frames(read_path=output_picture_path)
    remove_repeat_frames(read_path=output_picture_path)#此操作比较耗时,time = items_count ^ 2

def main():
    #提取视频帧
    flg = check_read_video_frames()
    if not flg:
        return 0

    #提取主要帧
    check_pick_stable_frames()

    #自动去除不需要的帧
    remove_frames()


if __name__ == "__main__":
    main()