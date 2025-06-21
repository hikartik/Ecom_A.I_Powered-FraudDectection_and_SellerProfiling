import numpy as np

class ReviewEnsembler:
    def __init__(self, similarity_weight=0.4, behavior_weight=0.6):
        self.similarity_weight = similarity_weight
        self.behavior_weight = behavior_weight

    def ensemble(self, similarity_labels, behavior_scores):
        # Fix: Use numpy's bincount for label frequency
        unique_labels, counts = np.unique(similarity_labels, return_counts=True)
        label_to_count = dict(zip(unique_labels, counts))

        normalized_similarity = [1.0 / label_to_count[label] for label in similarity_labels]

        final_scores = [
            float(self.similarity_weight * sim + self.behavior_weight * beh)
            for sim, beh in zip(normalized_similarity, behavior_scores)
        ]
        return final_scores