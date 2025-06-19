import os
import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

gallery_path = "./../gallery_images/"
embeddings = []

for fname in os.listdir(gallery_path):
    if fname.endswith(".jpg") or fname.endswith(".png"):
        image = preprocess(Image.open(os.path.join(gallery_path, fname))).unsqueeze(0).to(device)
        with torch.no_grad():
            emb = model.encode_image(image).cpu().numpy()
            embeddings.append(emb)

embeddings = np.vstack(embeddings)
np.save("./gallery_embeddings.npy", embeddings)
