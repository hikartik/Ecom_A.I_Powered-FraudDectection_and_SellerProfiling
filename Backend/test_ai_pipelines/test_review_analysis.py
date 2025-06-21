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

scorer = BatchReviewScorer()
final_scores = scorer.score(reviews)
print(final_scores)
