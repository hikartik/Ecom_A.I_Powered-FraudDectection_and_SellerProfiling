import torch
import clip
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VisionModel:
    def __init__(self, device='cpu'):
        self.model, self.preprocess = clip.load("ViT-B/32", device=device)
        self.device = device
        # Load gallery embeddings (precomputed)
        self.gallery_features = np.load("./gallery_embeddings.npy")

    def get_embedding(self, image):
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            return self.model.encode_image(image).cpu().numpy()

    def predict(self, image: Image.Image):
        emb = self.get_embedding(image)
        sims = cosine_similarity(emb, self.gallery_features)
        return float(np.max(sims))  # return best match score
