# Automatic Annotation

A multi-model framework for automatic image annotation and segmentation, integrating four state-of-the-art computer vision models. Generate COCO-format annotations from images with minimal human effort.

## Supported Models

| Model | Type | Description |
|-------|------|-------------|
| **YOLO** (Ultralytics) | Detection & Segmentation | Real-time object detection and instance segmentation with custom-trained weights. Run once on an image folder — fastest option. |
| **INSID3** | In-context Segmentation | Training-free few-shot segmentation using a frozen DINOv3 encoder. Provide a reference image + mask pair; segments the same class in target images. |
| **LocateAnything** (EagleVL) | Vision-Language Grounding | Parallel box decoding from natural language queries. Detect objects described by text prompts via a Qwen2-based VLM. No segmentation mask — bounding boxes only. |
| **SAM3** (Segment Anything 3) | Promptable Segmentation | Text-prompt segmentation using Meta's SAM3 model. Describe what you want to segment in natural language. |

## Project Structure

```
├── pkg/
│   ├── insid3/             # INSID3 — training-free in-context segmentation
│   ├── yolo/               # Ultralytics YOLO11
│   ├── eaglevl/            # LocateAnything — text-prompt grounding
│   └── sam3/               # SAM3 — text-prompt segmentation
├── src/
│   ├── annotation_use_yolo.ipynb        # YOLO auto-annotation
│   ├── annotation_use_insid3.ipynb      # INSID3 auto-annotation
│   ├── annotation_use_locany.ipynb      # LocateAnything auto-annotation
│   ├── annotation_use_sam3.ipynb        # SAM3 auto-annotation
│   ├── locateanything_worker.py         # Reusable LocateAnything inference worker
│   └── verify_coco_annotation.ipynb     # Verify generated annotations
├── scripts/
│   ├── build_env.sh                     # Create conda env + install base deps
│   ├── source_insid3_env.sh             # INSID3 dependencies + download weights
│   ├── source_yolo_env.sh               # YOLO package installation
│   ├── source_locany_env.sh             # LocateAnything package installation
│   ├── source_sam3_env.sh               # SAM3 dependencies
│   └── download_weights.py              # Generic weight download script
├── test/
│   ├── sam3_t.py                        # SAM3 minimal inference test
│   └── single_image_pred.ipynb          # LocateAnything single-image demo
├── modify_tool/                         # Dataset modification utilities
├── assets/                              # Example reference images & annotations
├── datasets/                            # Target dataset images & annotations
└── weights/                             # Model weight files (gitignored)
```

## Quick Start

### 1. Environment Setup

```bash
# Create base environment
bash scripts/build_env.sh

# Activate environment
conda activate auto_annotation

# Install model-specific dependencies (run what you need)
bash scripts/source_yolo_env.sh       # YOLO11
bash scripts/source_insid3_env.sh     # INSID3 + CRF + weights
bash scripts/source_sam3_env.sh       # SAM3
bash scripts/source_locany_env.sh     # LocateAnything (separate conda env)
```

### 2. Run Annotation

Open and run the corresponding Jupyter notebook in `src/`:

```bash
jupyter lab src/
```

| Notebook | Model | What You Provide | Output |
|----------|-------|-----------------|--------|
| `annotation_use_yolo.ipynb` | YOLO | Custom-trained `.pt` weights | BBox + instance segmentation masks |
| `annotation_use_insid3.ipynb` | INSID3 | Reference image + mask | Instance segmentation masks (polygon) |
| `annotation_use_locany.ipynb` | LocateAnything | Text prompts (e.g., "red box") | Bounding boxes (no masks) |
| `annotation_use_sam3.ipynb` | SAM3 | Text prompts (e.g., "red box") | Instance segmentation masks (polygon) |

All notebooks configure class labels via `class_config` — edit the dict to match your use case.

### 3. Verify Annotations

Use `src/verify_coco_annotation.ipynb` to visually inspect generated annotations before downstream use.

## Output Format

All models generate annotations in **COCO JSON format**:

```json
{
  "images": [{"id": 1, "file_name": "giftbox_1.png", "width": 640, "height": 480}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 0, "segmentation": [[x1,y1,x2,y2,...]], "bbox": [x,y,w,h], "area": 12345.0, "iscrowd": 0}],
  "categories": [{"id": 0, "name": "红盒子"}, {"id": 1, "name": "小物体"}, {"id": 2, "name": "绿色小盒子"}, {"id": 3, "name": "玩具车"}]
}
```

A `labels.txt` file is also generated alongside `annotations.json` for convenience.

## Requirements

- Python >= 3.8
- PyTorch >= 2.0 (CUDA recommended)
- See individual model `requirements.txt` / `pyproject.toml` for details

## License

This project integrates multiple open-source models. Refer to each subpackage for its respective license:
- **INSID3**: Based on DINOv3 (MIT)
- **YOLO11 (Ultralytics)**: AGPL-3.0
- **LocateAnything (EagleVL)**: Apache 2.0 / MIT
- **SAM3**: Apache 2.0
