import os
import torch
import clip
from PIL import Image
import numpy as np

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def compute_embedding(images: list[Image.Image]) -> np.ndarray:
    embeddings = []
    for image in images:
        image_tensor = preprocess(image).unsqueeze(0).to(device)  # shape: [1, C, H, W]
        with torch.no_grad():
            embedding = model.encode_image(image_tensor).cpu().numpy()  # shape: [1, embedding_dim]
        embeddings.append(embedding)
    return np.vstack(embeddings)  # shape: [len(images), embedding_dim]

def update_gallery_embedding(images: list[Image.Image], emb_path: str) -> None:
    if not images:
        print("⚠️ No images provided to update gallery.")
        return

    new_embedding = compute_embedding(images)

    if os.path.exists(emb_path):
        existing = np.load(emb_path)
        if existing.shape[1] != new_embedding.shape[1]:
            raise ValueError(f"Embedding dimension mismatch: existing {existing.shape[1]}, new {new_embedding.shape[1]}")

        updated = np.vstack([existing, new_embedding])
        print(f"Gallery embeddings updated: {existing.shape[0]} -> {updated.shape[0]} samples")
    else:
        updated = new_embedding
        print(f"Gallery embeddings created with {updated.shape[0]} samples")

    np.save(emb_path, updated)
    print("✅ Gallery updated with new given product images.")