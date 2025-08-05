import torch
try:
    import clip  # type: ignore
except Exception:
    clip = None
from PIL import Image
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MultimodalModel:
    def __init__(self, device: str = "cpu"):
        self.device = device
        if clip is not None:
            try:
                self.model, self.preprocess = clip.load("ViT-B/32", device=device)
            except Exception:
                self.model, self.preprocess = None, self._fallback_preprocess
        else:
            self.model, self.preprocess = None, self._fallback_preprocess

    def _fallback_preprocess(self, img: Image.Image) -> torch.Tensor:
        return torch.zeros(3, 224, 224)

    def predict(self, images: list[Image.Image], title: str, desc: str) -> float:
        if self.model is None:
            # Simple heuristic: average the vision and text heuristics.
            from .vision_model import VisionModel
            from .text_model import TextModel

            v_score = VisionModel(self.device).predict(images)
            t_score = TextModel().predict(title, desc)
            return float((v_score + t_score) / 2)

        image_tensors = [self.preprocess(img).unsqueeze(0) for img in images]
        image_batch = torch.cat(image_tensors, dim=0).to(self.device)

        text = f"{title}. {desc}"
        text_tokens = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_batch).cpu().numpy()
            text_features = self.model.encode_text(text_tokens).cpu().numpy()

        similarities = cosine_similarity(image_features, text_features)
        return float(np.mean(similarities))  # return average score
