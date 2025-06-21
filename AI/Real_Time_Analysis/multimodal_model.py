import torch
import clip
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MultimodalModel:
    def __init__(self, device='cpu'):
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        self.device = device

    def predict(self, images: list[Image.Image], title: str, desc: str) -> float:
        image_tensors = [self.preprocess(img).unsqueeze(0) for img in images]
        image_batch = torch.cat(image_tensors, dim=0).to(self.device)

        text = f"{title}. {desc}"
        text_tokens = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_batch).cpu().numpy()
            text_features = self.model.encode_text(text_tokens).cpu().numpy()

        similarities = cosine_similarity(image_features, text_features)
        return float(np.mean(similarities))  # return average score
