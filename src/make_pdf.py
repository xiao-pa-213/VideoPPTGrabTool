import os, re
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config import *
from tqdm import tqdm

def main():
    # 读取所有路径并排序
    image_paths = [os.path.join(output_picture_path, f) for f in os.listdir(output_picture_path) if f.endswith('.png')]
    image_paths.sort(
        key=lambda x: int(re.search(r'frame_(\d+)', x).group(1)) if re.search(r'frame_(\d+)', x) else 0)


    pdf_name = 'output_pdf.pdf'  # 输出的 PDF 文件名

    c = canvas.Canvas(os.path.join(output_pdf_path,pdf_name))

    progressbar = tqdm(total=len(image_paths),desc="正在生成pdf文件")
    for image_path in image_paths:
        try:
            img = Image.open(image_path)
            image_width, image_height = img.size

            # 计算最佳页面大小以适应图片
            page_width = image_width + 2 * 36  # 添加一些边距（36 点）
            page_height = image_height + 2 * 36  # 添加一些边距（36 点）

            # 设置当前页面大小
            c.setPageSize((page_width, page_height))

            c.drawImage(image_path, 36, 36, width=image_width, height=image_height)
            c.showPage()
        except Exception as e:
            print(f"Error processing image '{image_path}': {e}")
        progressbar.update(1)
    progressbar.close()
    print("生成pdf完成!")
    c.save()
    clean_images_in_path(pictemp_path)  # 清空pictemp文件夹

if __name__ == "__main__":
    main()