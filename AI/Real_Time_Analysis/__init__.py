from AI.Real_Time_Analysis.vision_model import VisionModel
from AI.Real_Time_Analysis.text_model import TextModel
from AI.Real_Time_Analysis.multimodal_model import MultimodalModel

import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

vision_model = VisionModel(device)
text_model = TextModel()
multimodal_model = MultimodalModel(device)
