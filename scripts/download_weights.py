#Download with ModelScope’s Python SDK
import os
import shutil
from modelscope import snapshot_download

model_dir = snapshot_download('kernelmind/auto-annotation-embody', cache_dir='weights')

# Move all files from weights/kernelmind/auto-annotation-embody/ to weights/
src = os.path.join('weights', 'kernelmind', 'auto-annotation-embody')
for fname in os.listdir(src):
    shutil.move(os.path.join(src, fname), os.path.join('weights', fname))

# Remove the empty kernelmind directory
shutil.rmtree(os.path.join('weights', 'kernelmind'))