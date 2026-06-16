source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate auto_annotation

pip install samexporter


cd pkg/sam3

pip install -e .

cd ../../