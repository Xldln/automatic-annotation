



conda create -n auto_annotation python=3.12 -y
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate auto_annotation
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt
