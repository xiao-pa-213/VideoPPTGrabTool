import os
from config import *
from tools import *

def check_all_paths():
    check_path(raw_video_file)
    check_path(output_picture_path)
    check_path(os.path.join(output_picture_path,"crashbin_auto"))
    check_path(os.path.join(output_picture_path,"crashbin_manual"))
    check_path(output_pdf_path)
    check_path(output_ppt_path)
    check_path(template_path)
    check_path(pictemp_path)
    print("Check finished")

def main():
    check_all_paths()

if __name__ == "__main__":
    main()