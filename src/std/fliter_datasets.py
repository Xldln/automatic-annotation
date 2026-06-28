import os
import re
from pathlib import Path
import shutil

os.chdir("../../")

# def main():

#     images_path = Path("datasets/standard_datasets/images")
#     anno_dir = Path("datasets/standard_datasets/annotations")

#     anno_list = list(anno_dir.glob("*.json"))
#     video_list = [x.name for x in images_path.iterdir() if x.is_dir()]

#     use_list = []
#     for anno in anno_list:
#         match = re.search(r"annotations_(\d+)\.json", anno.name)
#         if match:
#             video_id = match.group(1)
#             use_list.append(video_id)

#     unuse = set(use_list) - set(video_list)

#     for un in unuse:
#         file_path = anno_dir / f"annotations_{un}.json"
#         if file_path.exists():  
#             print(f"正在删除无对应视频的标注文件: {file_path}")
#             os.remove(file_path) 



## from anntation del video floder
def main():

    images_path = Path("datasets/standard_datasets/images")
    anno_dir = Path("datasets/standard_datasets/annotations")


    anno_list = list(anno_dir.glob("*.json"))
    video_list = [x.name for x in images_path.iterdir() if x.is_dir()]

    use_list = []
    for anno in anno_list:
        match = re.search(r"annotations_(\d+)\.json", anno.name)
        if match:
            video_id = match.group(1)
            use_list.append(video_id)
        else:
            continue

    unuse = set(video_list) - set(use_list)

    for un in unuse:
        file_path = images_path / un
        if file_path.exists():  
            print(f"正在删除未标注的文件夹: {file_path}")
            shutil.rmtree(file_path) 






if __name__ == "__main__":
    main()
