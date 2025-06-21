from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import AgglomerativeClustering
import numpy as np

class SimilarityGrouper:
    def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.75):
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    def get_groups(self, reviews):
        embeddings = self.model.encode(reviews, convert_to_tensor=True)
        similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()

        clustering = AgglomerativeClustering(n_clusters=None, metric='precomputed', linkage='average', distance_threshold=1 - self.threshold)
        labels = clustering.fit_predict(1 - similarity_matrix)

        grouped_reviews = {}
        for idx, label in enumerate(labels):
            grouped_reviews.setdefault(label, []).append(reviews[idx])

        return grouped_reviews, labels