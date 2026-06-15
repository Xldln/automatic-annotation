# Automatic Annotation（自动标注）

一个多模型融合的自动图像标注与分割框架，集成了四种前沿计算机视觉模型。用户只需少量人工干预，即可从图像自动生成 COCO 格式的标注数据。

## 支持的模型

| 模型 | 类型 | 说明 |
|-------|------|-------------|
| **INSID3** | 上下文分割 (In-context Segmentation) | 基于冻结 DINOv3 编码器的免训练少样本分割。通过参考图像-掩码对即可分割新类别，无需微调。 |
| **YOLO** (Ultralytics) | 检测与分割 | 实时目标检测与实例分割。包含针对特定任务（如礼盒检测）的自定义训练权重。 |
| **LocateAnything** (EagleVL) | 视觉语言定位 | 基于自然语言描述的并行框解码。通过文本提示定位目标物体，基于 Qwen2 视觉语言模型。 |
| **SAM3** (Segment Anything 3) | 可提示分割 | 可导出的 ONNX 通用分割模型，适用于各种场景的掩码生成。 |

## 项目结构

```
├── pkg/
│   ├── insid3/             # INSID3 上下文分割模型
│   │   ├── models/         # 模型实现（冻结 DINOv3 编码器）
│   │   ├── datasets/       # 数据集加载器（COCO、LVIS、PASCAL-Part、iSAID 等）
│   │   ├── utils/          # 聚类、评估指标、可视化、精细化后处理工具
│   │   ├── opts.py         # 命令行参数解析器
│   │   └── inference_segmentation.py  # 评估/推理脚本
│   ├── yolo/               # Ultralytics YOLO11（检测 + 分割）
│   │   └── ultralytics/    # 完整 Ultralytics 框架
│   └── eaglevl/            # LocateAnything 视觉语言定位
│       ├── model/          # LocateAnything 模型（Qwen2 + MoonViT）
│       ├── sp_utils/       # 序列并行工具（环状/flash attention）
│       ├── utils/          # 推理工具与配置
│       ├── train/          # 训练流程（含 FastSeek）
│       └── patch/          # 性能优化补丁（FP8、融合算子、packing）
├── src/
│   ├── annotation_use_insid3.ipynb   # 笔记本：INSID3 标注
│   ├── annotation_use_locany.ipynb   # 笔记本：LocateAnything 标注
│   ├── annotation_use_sam3.ipynb     # 笔记本：SAM3 标注
│   ├── annotation_use_yolo.ipynb     # 笔记本：YOLO 标注
│   └── verify_coco_annotation.ipynb  # 笔记本：验证生成的 COCO 标注
├── scripts/
│   ├── build_env.sh                   # 创建 conda 环境 + 安装基础依赖
│   ├── source_insid3_env.sh           # 安装 INSID3 依赖 + 下载权重
│   ├── source_locany_env.sh           # 安装 LocateAnything 包
│   ├── source_sam3_env.sh             # 安装 SAM3 依赖
│   └── source_yolo_env.sh             # 安装 YOLO 包
└── weights/                           # 模型权重文件（通过 .gitignore 排除）
```

## 快速开始

### 1. 环境配置

```bash
# 创建基础环境
bash scripts/build_env.sh

# 激活环境
conda activate auto_annotation

# 安装各模型的依赖
bash scripts/source_insid3_env.sh   # INSID3 + CRF + 权重下载
bash scripts/source_yolo_env.sh     # YOLO11
bash scripts/source_locany_env.sh   # LocateAnything
bash scripts/source_sam3_env.sh     # SAM3
```

### 2. 运行标注

打开 `src/` 下对应的 Jupyter notebook 并运行：

```bash
jupyter lab src/
```

- `annotation_use_yolo.ipynb` — 目标检测 / 实例分割
- `annotation_use_insid3.ipynb` — 少样本上下文分割
- `annotation_use_locany.ipynb` — 文本提示定位
- `annotation_use_sam3.ipynb` — 通用掩码生成

### 3. 验证标注

使用 `src/verify_coco_annotation.ipynb` 可视化验证生成的 COCO 格式标注，确保质量。

## 输出格式

所有模型生成的标注均为 **COCO JSON 格式**：

```json
{
  "images": [{"id": 1, "file_name": "...", "width": 640, "height": 480}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 1, "segmentation": [...], "bbox": [...], "area": ...}],
  "categories": [{"id": 1, "name": "礼盒"}]
}
```

## 系统要求

- Python >= 3.8
- PyTorch >= 2.0（推荐使用 CUDA）
- 各模型详细依赖请参见对应子包的 `requirements.txt` / `pyproject.toml`

## 许可证

本项目集成了多个开源模型，请参考各子包对应的许可证：
- **INSID3**: 基于 DINOv3（MIT）
- **YOLO11 (Ultralytics)**: AGPL-3.0
- **LocateAnything (EagleVL)**: Apache 2.0 / MIT
- **SAM3**: Apache 2.0
