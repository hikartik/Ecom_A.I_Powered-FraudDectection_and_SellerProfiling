import torch
import clip
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VisionModel:
    def __init__(self, device='cpu'):
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        self.device = device
        self.gallery_features = np.load("./gallery_embeddings.npy")

    def get_embedding(self, images: list[Image.Image]) -> np.ndarray:
        image_tensors = [self.preprocess(img).unsqueeze(0) for img in images]
        image_batch = torch.cat(image_tensors, dim=0).to(self.device)
        with torch.no_grad():
            embeddings = self.model.encode_image(image_batch).cpu().numpy()
        return embeddings

    def predict(self, images: list[Image.Image]) -> float:
        embeddings = self.get_embedding(images)
        sims = cosine_similarity(embeddings, self.gallery_features)
        best_scores = np.max(sims, axis=1)  # one per image
        return float(np.mean(best_scores))  # return average score