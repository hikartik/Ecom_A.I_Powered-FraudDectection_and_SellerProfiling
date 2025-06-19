import torch
import clip
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity

class MultimodalModel:
    def __init__(self, device='cpu'):
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        self.device = device

    def predict(self, image: Image.Image, title: str, desc: str):
        text = f"{title}. {desc}"
        image_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
        text_tokens = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image_tensor).cpu().numpy()
            text_features = self.model.encode_text(text_tokens).cpu().numpy()
        return float(cosine_similarity(image_features, text_features)[0][0])
