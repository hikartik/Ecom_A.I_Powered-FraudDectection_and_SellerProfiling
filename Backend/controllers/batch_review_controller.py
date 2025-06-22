# controllers/batch_review_controller.py
from datetime import datetime
from bson import ObjectId
from Backend.utils.database import db
from AI.Batch_Analysis.Review_Analyzer.review_scorer import BatchReviewScorer

reviews_col = db["reviews"]

async def batch_update_review_scores():
    """
    Fetches all reviews, computes new scores, and updates each document.
    """
    print(f"🔔 Running batch_update_review_scores at {datetime.utcnow()}")

    # 1. load all reviews comments and ids
    cursor = reviews_col.find({})
    reviews = []  # list of tuples (id, comment)
    for doc in cursor:
        reviews.append((str(doc["_id"]), doc.get("comment", "")))

    if not reviews:
        print("No reviews to update.")
        return {"updated": 0}

    # 2. compute scores
    comments = [c for _, c in reviews]
    scorer = BatchReviewScorer()
    scores = scorer.score(comments)

    # 3. update each review
    updated = 0
    for (rid, _), score in zip(reviews, scores):
        result = reviews_col.update_one(
            {"_id": ObjectId(rid)},
            {"$set": {"rating_score": float(score), "created_at": datetime.utcnow()}}
        )
        if result.modified_count:
            updated += 1
    print(f"✅ batch_update_review_scores updated {updated} reviews.")
    return {"updated": updated}