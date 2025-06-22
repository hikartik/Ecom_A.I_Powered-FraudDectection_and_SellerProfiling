# controllers/batch_review_controller.py
from datetime import datetime
from bson import ObjectId
from Backend.utils.database import db
from AI.Batch_Analysis.Review_Analyzer.review_scorer import BatchReviewScorer
import logging

# Set up logging
logger = logging.getLogger(__name__)

reviews_col = db["reviews"]

async def batch_update_review_scores():
    """
    Fetches all reviews, computes new scores, and updates each document.
    """
    logger.info(f"🔔 Running batch_update_review_scores at {datetime.utcnow()}")

    try:
        # 1. load all reviews comments and ids
        cursor = reviews_col.find({})
        reviews = []  # list of tuples (id, comment)
        for doc in cursor:
            reviews.append((str(doc["_id"]), doc.get("comment", "")))

        if not reviews:
            logger.info("No reviews to update.")
            return {"updated": 0}

        logger.info(f"Found {len(reviews)} reviews to process")

        # 2. compute scores
        comments = [c for _, c in reviews]
        scorer = BatchReviewScorer()
        scores = scorer.score(comments)

        # 3. update each review
        updated = 0
        for (rid, _), score in zip(reviews, scores):
            result = reviews_col.update_one(
                {"_id": ObjectId(rid)},
                {"$set": {"rating_score": float(score), "updated_at": datetime.utcnow()}}
            )
            if result.modified_count:
                updated += 1
                logger.debug(f"Updated review {rid} with score {score:.4f}")
        
        logger.info(f"✅ batch_update_review_scores updated {updated} reviews.")
        return {"updated": updated}
        
    except Exception as e:
        logger.error(f"❌ Error in batch_update_review_scores: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {"updated": 0, "error": str(e)}