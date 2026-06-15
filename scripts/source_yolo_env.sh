

source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate auto_annotation

cd pkg/yolo

pip install -e .

cd ../../