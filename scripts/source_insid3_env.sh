

source "$(conda info --base)/etc/profile.d/conda.sh"

conda activate auto_annotation

cd pkg/insid3

pip install -r requirements.txt

git clone https://github.com/netw0rkf10w/CRF.git

cd CRF

python setup.py install

cd ../../../

mkdir -p weights/insid3 && cd weights/insid3


wget https://yubinux.cn/tmp/pt/dinov3_vitl16_pretrain_lvd1689m-8aa4cbdd.pth 

cd ../../