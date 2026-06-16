import torch
import matplotlib.pyplot as plt
from PIL import Image

from sam3.model_builder import build_sam3_image_model
from sam3.model.sam3_image_processor import Sam3Processor
from sam3.visualization_utils import plot_results
from torchvision import transforms

torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False


model = build_sam3_image_model()
processor = Sam3Processor(model)

# transform = transforms.ToTensor()

# image = Image.open("assets/images/test_image.jpg")
# image_tensor = transform(image)

# image_tensor = image_tensor.to(dtype=torch.float32)


# print("image_tensor dtype:", image_tensor.dtype)
# inference_state = processor.set_image(image_tensor)

# inference_state = processor.set_text_prompt(state=inference_state, prompt="child")


# plot_results(image, inference_state)
# plt.show()  