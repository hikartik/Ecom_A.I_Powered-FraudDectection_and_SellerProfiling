# Backend/controllers/batch_seller_controller.py

import os
import sys
import torch
from datetime import datetime
from bson import ObjectId
from Backend.utils.database import db
import logging

# Set up logging
logger = logging.getLogger(__name__)

# make sure the AI module import works
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "./../..")
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from AI.Batch_Analysis.Seller_Profiling_Engine.seller_garph_profiler import SellerGraphModel

# Mongo collections
users_col    = db["users"]
products_col = db["products"]
reviews_col  = db["reviews"]

def to_tensor(x):
    """Convert float/int or list to a torch Tensor shaped [N,1]."""
    if isinstance(x, torch.Tensor):
        return x.float()
    if isinstance(x, (float, int)):
        return torch.tensor([[float(x)]], dtype=torch.float32)
    if isinstance(x, (list, tuple)):
        if not x:  # Handle empty lists
            return torch.tensor([[0.0]], dtype=torch.float32)
        return torch.tensor(x, dtype=torch.float32).view(-1, 1)
    raise ValueError(f"Unsupported type: {type(x)}")

async def batch_update_seller_scores():
    """
    Runs the SellerGraphModel on each seller and updates their `score` field.
    """
    logger.info(f"🔔 Running batch_update_seller_scores at {datetime.utcnow()}")
    model = SellerGraphModel(hidden_channels=32)
    updated_count = 0
    error_count = 0

    # iterate all sellers
    for user in users_col.find({"type": "seller"}):
        sid = str(user["_id"])

        try:
            # seller feature from existing score
            seller_feat = to_tensor(user.get("score", 0.0))

            # gather product features and their review scores
            product_feats = []
            for p in products_col.find({"seller_id": sid}):
                # collect review scores for this product
                review_scores = [
                    r.get("rating_score", 0.0)
                    for r in reviews_col.find({
                        "product_id": str(p["_id"])
                    })
                ]
                
                # Ensure we have at least one review score (even if 0.0)
                if not review_scores:
                    review_scores = [0.0]
                
                product_feats.append({
                    "vision":     to_tensor(p.get("vision_score", 0.0)),
                    "text":       to_tensor(p.get("text_score",   0.0)),
                    "multimodal": to_tensor(p.get("multimodal_score", 0.0)),
                    "ensemble":   to_tensor(p.get("ensemble_score",   0.0)),
                    "reviews":    [to_tensor(rs) for rs in review_scores],
                })

            # If no products, create a dummy product
            if not product_feats:
                product_feats = [{
                    "vision":     to_tensor(0.0),
                    "text":       to_tensor(0.0),
                    "multimodal": to_tensor(0.0),
                    "ensemble":   to_tensor(0.0),
                    "reviews":    [to_tensor(0.0)],
                }]

            # build input for the model and run
            inp = {
                "seller_features":   seller_feat,
                "product_features": product_feats
            }
            
            risk_tensor = model(inp)
            new_score = float(risk_tensor.item())

            # update the user document
            res = users_col.update_one(
                {"_id": ObjectId(sid)},
                {"$set": {"score": new_score, "updated_at": datetime.utcnow()}}
            )
            if res.modified_count:
                updated_count += 1
                logger.info(f"✅ Updated seller {sid} with score {new_score:.4f}")

        except Exception as e:
            error_count += 1
            logger.error(f"❌ Model failed for seller {sid}: {e}")
            continue

    logger.info(f"✅ batch_update_seller_scores completed: {updated_count} updated, {error_count} errors")
    return {"updated": updated_count, "errors": error_count}
