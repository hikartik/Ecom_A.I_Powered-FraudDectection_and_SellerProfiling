from .similarity_grouper import SimilarityGrouper
from .behavior_scorer import ReviewBehaviorScorer
from .ensemble_scorer import ReviewEnsembler

class BatchReviewScorer:
    def __init__(self):
        self.grouper = SimilarityGrouper()
        self.behavior_scorer = ReviewBehaviorScorer()
        self.ensembler = ReviewEnsembler()

    def score(self, reviews):
        grouped_reviews, similarity_labels = self.grouper.get_groups(reviews)
        behavior_scores = self.behavior_scorer.score_reviews(reviews)
        final_scores = self.ensembler.ensemble(similarity_labels, behavior_scores)
        return final_scores