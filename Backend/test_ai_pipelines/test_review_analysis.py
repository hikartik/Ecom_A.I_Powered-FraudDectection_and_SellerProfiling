import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../.."))
sys.path.insert(0, project_root)

from AI.Batch_Analysis.Review_Analyzer.review_scorer import BatchReviewScorer

reviews = [
    "Great product! Highly recommend it!",
    "Amazing product. Must buy.",
    "Worst product I have ever used.",
    "Excellent product! Highly recommend it!",
    "Worst product I have ever used.",
]


def test_batch_review_scorer():
    scorer = BatchReviewScorer()
    final_scores = scorer.score(reviews)
    assert len(final_scores) == len(reviews)
    for score in final_scores:
        assert 0.0 <= score <= 1.0
