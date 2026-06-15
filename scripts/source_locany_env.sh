
source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate auto_annotation


cd pkg/eaglevl

pip install -e .

cd ../../