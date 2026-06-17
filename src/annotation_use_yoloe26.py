from ultralytics import YOLOE



import json
from pathlib import Path
from skimage import measure
import numpy as np



def make_coco_annotation(predict_results, model, save_path):
    """
    Convert YOLO segmentation predict results to COCO format annotation.json
    
    Args:
        predict_results: list of ultralytics.engine.results.Results
        model: YOLO model (for model.names)
        save_path: Path to save the annotation.json
    """
    class_names = model.names  # {0: 'class0', 1: 'class1', ...}
    
    coco_output = {
        "images": [],
        "annotations": [],
        "categories": [
            {"id": int(cat_id), "name": name, "supercategory": "object"}
            for cat_id, name in class_names.items()
        ],
    }
    
    ann_id = 1
    
    for img_id, result in enumerate(predict_results, start=1):
        height, width = result.orig_shape
        image_path = Path(result.path)
        
        coco_output["images"].append({
            "id": img_id,
            "file_name": image_path.name,
            "width": width,
            "height": height,
        })
        
        if result.masks is None:
            print(f"  ⚠ No masks found for {image_path.name}, skipping...")
            continue
        
        boxes_xyxy = result.boxes.xyxy.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        confidences = result.boxes.conf.cpu().numpy()
        
        for i, mask_polygon in enumerate(result.masks.xy):
            x1, y1, x2, y2 = boxes_xyxy[i]
            w = x2 - x1
            h = y2 - y1
            
            segmentation = mask_polygon.flatten().tolist()
            
            poly = mask_polygon
            area = 0.5 * abs(np.dot(poly[:, 0], np.roll(poly[:, 1], 1)) -
                            np.dot(poly[:, 1], np.roll(poly[:, 0], 1)))
            
            coco_output["annotations"].append({
                "id": ann_id,
                "image_id": img_id,
                "category_id": int(class_ids[i]),
                "segmentation": [segmentation],
                "bbox": [float(x1), float(y1), float(w), float(h)],
                "area": float(area),
                "iscrowd": 0
            })
            ann_id += 1
    
    # Save
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(coco_output, f, indent=2, ensure_ascii=False)

    labels_path = save_path.parent / "labels.txt"
    with open(labels_path, "w", encoding="utf-8") as f_labels:

        for cat_id in sorted(class_names.keys()):
            f_labels.write(f"{class_names[cat_id]}\n")
    
    num_imgs = len(coco_output["images"])
    num_anns = len(coco_output["annotations"])
    num_cats = len(coco_output["categories"])
    print(f"✅ COCO annotation saved to {save_path}")
    print(f"   images={num_imgs}, annotations={num_anns}, categories={num_cats}")





if __name__ == "__main__":

    model_path = "../weights/yoloe/yoloe-26x-seg.pt"

    model = YOLOE(model_path)

    model.set_classes(["red box", "small object","green small box","toy car"])

    image_path = "../datasets/giftbox_task/images"

    annotation_file = Path("../datasets/giftbox_task/annotations/annotations_yoloe.json")

    if not annotation_file.exists():
        annotation_file.parent.mkdir(parents=True, exist_ok=True)
        annotation_file.touch()


    predict_results = model(image_path, device="cuda:0")


    make_coco_annotation(predict_results, model, annotation_file)




