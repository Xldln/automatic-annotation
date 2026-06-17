# Automatic Annotation（自动标注）

一个多模型融合的自动图像标注与分割框架，集成了四种前沿计算机视觉模型。用户只需少量人工干预，即可从图像自动生成 COCO 格式的标注数据。

## 支持的模型

| 模型 | 类型 | 说明 |
|-------|------|-------------|
| **YOLO** (Ultralytics) | 检测与分割 | 实时目标检测与实例分割，可使用自定义训练权重。在图片文件夹上推理一次即可完成全部标注——速度最快。 |
| **INSID3** | 上下文分割 (In-context Segmentation) | 基于冻结 DINOv3 编码器的免训练少样本分割。提供一张参考图像 + 掩码对，即可在目标图像中分割同类物体。 |
| **LocateAnything** (EagleVL) | 视觉语言定位 | 基于自然语言描述的并行框解码。用文本提示定位物体，基于 Qwen2 视觉语言模型。仅输出边界框，无分割掩码。 |
| **SAM3** (Segment Anything 3) | 文本提示分割 | 使用 Meta SAM3 模型的文本提示分割。用自然语言描述想要分割的内容。 |

## 项目结构

```
├── pkg/
│   ├── insid3/             # INSID3 — 免训练上下文分割
│   ├── yolo/               # Ultralytics YOLO11
│   ├── eaglevl/            # LocateAnything — 文本提示定位
│   └── sam3/               # SAM3 — 文本提示分割
├── src/
│   ├── annotation_use_yolo.ipynb        # YOLO 自动标注
│   ├── annotation_use_insid3.ipynb      # INSID3 自动标注
│   ├── annotation_use_locany.ipynb      # LocateAnything 自动标注
│   ├── annotation_use_sam3.ipynb        # SAM3 自动标注
│   ├── locateanything_worker.py         # LocateAnything 可复用推理 worker
│   └── verify_coco_annotation.ipynb     # 验证生成标注
├── scripts/
│   ├── build_env.sh                     # 创建 conda 环境 + 安装基础依赖
│   ├── source_insid3_env.sh             # INSID3 依赖 + 权重下载
│   ├── source_yolo_env.sh               # YOLO 包安装
│   ├── source_locany_env.sh             # LocateAnything 包安装
│   ├── source_sam3_env.sh               # SAM3 依赖
│   └── download_weights.py              # 通用权重下载脚本
├── test/
│   ├── sam3_t.py                        # SAM3 最小推理测试
│   └── single_image_pred.ipynb          # LocateAnything 单图推理示例
├── modify_tool/                         # 数据集修改工具
├── assets/                              # 示例参考图像与标注
├── datasets/                            # 目标数据集图像与标注
└── weights/                             # 模型权重文件（gitignore）
```

## 快速开始

### 1. 环境配置

```bash
# 创建基础环境
bash scripts/build_env.sh

# 激活环境
conda activate auto_annotation

# 按需安装各模型依赖
bash scripts/source_yolo_env.sh       # YOLO11
bash scripts/source_insid3_env.sh     # INSID3 + CRF + 权重
bash scripts/source_sam3_env.sh       # SAM3
bash scripts/source_locany_env.sh     # LocateAnything（独立 conda 环境）
```

### 2. 运行标注

打开 `src/` 下对应的 Jupyter notebook 并运行：

```bash
jupyter lab src/
```

| Notebook | 模型 | 你需要提供 | 输出 |
|----------|------|-----------|------|
| `annotation_use_yolo.ipynb` | YOLO | 自定义训练的 `.pt` 权重 | 边界框 + 实例分割掩码 |
| `annotation_use_insid3.ipynb` | INSID3 | 参考图像 + 掩码 | 实例分割掩码（多边形） |
| `annotation_use_locany.ipynb` | LocateAnything | 文本提示（如 "red box"）| 边界框（无掩码） |
| `annotation_use_sam3.ipynb` | SAM3 | 文本提示（如 "red box"）| 实例分割掩码（多边形） |

所有 notebook 均通过 `class_config` 配置类别标签——修改字典即可适配你的使用场景。

### 3. 验证标注

使用 `src/verify_coco_annotation.ipynb` 可视化验证生成的标注结果，确保质量。

## 输出格式

所有模型生成的标注均为 **COCO JSON 格式**：

```json
{
  "images": [{"id": 1, "file_name": "giftbox_1.png", "width": 640, "height": 480}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 0, "segmentation": [[x1,y1,x2,y2,...]], "bbox": [x,y,w,h], "area": 12345.0, "iscrowd": 0}],
  "categories": [{"id": 0, "name": "red box"}, {"id": 1, "name": "small object"}, {"id": 2, "name": "green samll box"}, {"id": 3, "name": "toy car"}]
}
```

同时会在 `annotations.json` 旁边生成 `labels.txt` 文件，方便查阅。

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
