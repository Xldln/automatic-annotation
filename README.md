# Automatic Annotation

A multi-model framework for automatic image annotation and segmentation, integrating four state-of-the-art computer vision models. Generate COCO-format annotations from images with minimal human effort.

## Supported Models

| Model | Type | Description |
|-------|------|-------------|
| **INSID3** | In-context Segmentation | Training-free few-shot segmentation using a frozen DINOv3 encoder. Segments novel classes from reference image-mask pairs without fine-tuning. |
| **YOLO** (Ultralytics) | Detection & Segmentation | Real-time object detection and instance segmentation. Includes custom trained weights for specific tasks (e.g., giftbox detection). |
| **LocateAnything** (EagleVL) | Vision-Language Grounding | Parallel box decoding from natural language queries. Locates objects described by text prompts via a Qwen2-based vision-language model. |
| **SAM3** (Segment Anything 3) | Promptable Segmentation | Exportable ONNX-based segmentation model for general-purpose mask generation. |

## Project Structure

```
├── pkg/
│   ├── insid3/             # INSID3 in-context segmentation model
│   │   ├── models/         # Model implementation (frozen DINOv3 encoder)
│   │   ├── datasets/       # Dataset loaders (COCO, LVIS, PASCAL-Part, iSAID, etc.)
│   │   ├── utils/          # Clustering, metrics, visualization, refinement utilities
│   │   ├── opts.py         # CLI argument parser
│   │   └── inference_segmentation.py  # Evaluation/inference script
│   ├── yolo/               # Ultralytics YOLO11 (detection + segmentation)
│   │   └── ultralytics/    # Full Ultralytics framework
│   └── eaglevl/            # LocateAnything vision-language grounding
│       ├── model/          # LocateAnything model (Qwen2 + MoonViT)
│       ├── sp_utils/       # Sequence parallelism utilities (ring/flash attention)
│       ├── utils/          # Inference utilities and configs
│       ├── train/          # Training pipeline with FastSeek
│       └── patch/          # Performance patches (FP8, fused ops, packing)
├── src/
│   ├── annotation_use_insid3.ipynb   # Notebook: INSID3 annotation
│   ├── annotation_use_locany.ipynb   # Notebook: LocateAnything annotation
│   ├── annotation_use_sam3.ipynb     # Notebook: SAM3 annotation
│   ├── annotation_use_yolo.ipynb     # Notebook: YOLO annotation
│   └── verify_coco_annotation.ipynb  # Notebook: verify generated COCO annotations
├── scripts/
│   ├── build_env.sh                   # Create conda environment + install base deps
│   ├── source_insid3_env.sh           # Setup INSID3 dependencies + download weights
│   ├── source_locany_env.sh           # Install LocateAnything package
│   ├── source_sam3_env.sh             # Install SAM3 dependencies
│   └── source_yolo_env.sh             # Install YOLO package
└── weights/                           # Model weight files (via .gitignore)
```

## Quick Start

### 1. Environment Setup

```bash
# Create base environment
bash scripts/build_env.sh

# Activate environment
conda activate auto_annotation

# Install model-specific dependencies
bash scripts/source_insid3_env.sh   # INSID3 + CRF + weights
bash scripts/source_yolo_env.sh     # YOLO11
bash scripts/source_locany_env.sh   # LocateAnything
bash scripts/source_sam3_env.sh     # SAM3
```

### 2. Run Annotation

Open and run the corresponding Jupyter notebook in `src/`:

```bash
jupyter lab src/
```

- `annotation_use_yolo.ipynb` — Object detection / instance segmentation
- `annotation_use_insid3.ipynb` — Few-shot in-context segmentation
- `annotation_use_locany.ipynb` — Text-prompted grounding
- `annotation_use_sam3.ipynb` — General-purpose mask generation

### 3. Verify Annotations

Use `src/verify_coco_annotation.ipynb` to visually verify generated COCO-format annotations before use.

## Output Format

All models generate annotations in **COCO JSON format**:

```json
{
  "images": [{"id": 1, "file_name": "...", "width": 640, "height": 480}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 1, "segmentation": [...], "bbox": [...], "area": ...}],
  "categories": [{"id": 1, "name": "red box"}]
}
```

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
