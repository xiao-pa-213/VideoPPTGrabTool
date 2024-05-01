import subprocess
import os
from config import *
from tools import clean_file_in_path

#用于生成ts测试文件
def main():
    input_video_path = raw_video_path
    output_dir = ts_file_path

    # 每个切片的时长（秒）
    segment_duration = 3

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    clean_file_in_path(output_dir,"*.ts")

    # 设置输出文件的模式，例如：segment_%03d.ts，表示从001开始递增
    segment_filename = 'segment_%04d.ts'

    # 构建FFmpeg命令
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video_path,  # 输入文件
        '-segment_time', str(segment_duration),  # 每个切片的时长
        '-segment_format', 'ts',  # 指定输出格式为TS
        '-c', 'copy',  # 使用复制模式，避免重新编码
        '-f', 'segment',
        '-map', '0',  # 选择所有流（视频、音频等）
        os.path.join(output_dir, segment_filename)  # 输出文件模式
    ]

    # 使用subprocess运行FFmpeg命令
    subprocess.run(ffmpeg_command)

if __name__ == "__main__":
    main()

    #ffmpeg -y -i data\raw_video\动物检疫检验学_2023-11-09第1节-高清.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb abc.ts
    #ffmpeg -i data\raw_video\动物检疫检验学_2023-11-09第1节-高清.mp4 -c copy -map 0 -f segment -segment_list playlist.m3u8 -segment_time 5 data\ts_file\abc%03d.ts