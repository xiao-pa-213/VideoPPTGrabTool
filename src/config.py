# config.py
# 保存全局变量

#提取视频帧采用的时间间隔N
garb_interval_n_seconds = 5 #默认5秒，过大会导致提取漏页，过小会导致处理时间较长，本地缓存占用较大

#视频文件名
raw_video_name = "动物检疫检验学_2023-11-09第1节-高清.mp4"#请将此项修改为网课视频的文件名

#内置路径参数，无需改动
raw_video_file = "../data/raw_video"
raw_video_path = raw_video_file + '/' + raw_video_name
output_picture_path = "../data/output_picture"
output_ppt_path = "../data/output_ppt"
output_pdf_path = "../data/output_pdf"
pictemp_path = "../data/pic_temp"
template_path = "../data/template"