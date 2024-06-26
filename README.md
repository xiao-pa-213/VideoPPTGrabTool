# 视频PPT截取工具
这是一个可以自动从网课视频中截取PPT画面并输出为pdf、ppt等格式的工具

## 功能
+ 以固定间隔提取视频帧，导出为png图片
+ 自动筛选符合网课PPT演示的视频帧
+ 用图片序列生成pptx或pdf格式文件

## 使用方法
1. 在工程根目录VideoPPTGrabTool/ 打开cmd，安装python环境依赖。  
```shell
    pip install -r requirements.txt
```
   
2. 检查缓存文件夹是否已经创建，若data文件夹下各文件夹完整可跳过这一步
```shell
    python src/check_paths.py
```
```shell
data
├───output_pdf
├───output_picture
│   ├───crashbin_auto
│   └───crashbin_manual
├───output_ppt
├───pic_temp
├───raw_video
└───template
```
3. 将要处理的视频文件放入data/1_raw_video/ ，若路径不存在可参考上一步或手动创建

4. 打开src/config.py ，修改相关参数  

5. 运行src/capture_picture.py 。此时会在data/output_picture 文件夹下产生视频中PPT内容相关的图片，请手动删除一些您不需要的图片。（可以右键删除也可顺手拖入crashbin_manual文件夹)
```shell
    python src/capture_picture.py
```

6. 此时data/output_picture 文件夹下应当存放有你需要的所有图片序列。  
运行src/下的make_pdf.py 或make_ppt.py 可以生成pdf/pptx文件
```shell
    python src/make_pdf.py
```

```shell
    python src/make_ppt.py
```

7. 最后生成的文件在data/ 下的output_pdf 或output_ppt 内。

## 参考
[1] 【视频提取PPT软件】微光萌生 Gleamoe Peanut 2023 https://zhuanlan.zhihu.com/p/619717101  
[2] B站 【用Python从视频里面扒PPT？】 https://www.bilibili.com/video/BV1RN4y1y7Kk/
