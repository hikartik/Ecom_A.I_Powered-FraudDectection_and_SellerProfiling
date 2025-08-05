try:
    from sentence_transformers import SentenceTransformer, util
    from sklearn.cluster import AgglomerativeClustering
except Exception:  # pragma: no cover - dependencies may be missing
    SentenceTransformer = None
    util = None
    AgglomerativeClustering = None
import numpy as np

class SimilarityGrouper:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', threshold: float = 0.75):
        self.threshold = threshold
        if SentenceTransformer is not None:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception:
                self.model = None
        else:
            self.model = None

    def get_groups(self, reviews):
        if self.model is None or util is None or AgglomerativeClustering is None:
            grouped_reviews = {}
            labels = np.zeros(len(reviews), dtype=int)
            next_label = 0
            for i, review in enumerate(reviews):
                for label, items in grouped_reviews.items():
                    if review in items:
                        labels[i] = label
                        items.append(review)
                        break
                else:
                    grouped_reviews[next_label] = [review]
                    labels[i] = next_label
                    next_label += 1
            return grouped_reviews, labels

        embeddings = self.model.encode(reviews, convert_to_tensor=True)
        similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings).cpu().numpy()

        clustering = AgglomerativeClustering(
            n_clusters=None,
            metric='precomputed',
            linkage='average',
            distance_threshold=1 - self.threshold,
        )
        labels = clustering.fit_predict(1 - similarity_matrix)

        grouped_reviews = {}
        for idx, label in enumerate(labels):
            grouped_reviews.setdefault(label, []).append(reviews[idx])

        return grouped_reviews, labels
    