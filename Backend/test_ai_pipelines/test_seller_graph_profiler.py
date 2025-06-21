import os
import sys
import torch

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../.."))
sys.path.insert(0, project_root)

from AI.Batch_Analysis.Seller_Profiling_Engine.seller_garph_profiler import SellerGraphModel

def to_tensor(x):
    # Convert Python float or list to tensor with shape [1, 1] and dtype float32
    if isinstance(x, torch.Tensor):
        return x.float()  # Already tensor
    elif isinstance(x, (float, int)):
        return torch.tensor([[float(x)]], dtype=torch.float32)
    elif isinstance(x, (list, tuple)):
        # Convert list of floats to tensor shape [len, 1]
        return torch.tensor(x, dtype=torch.float32).view(-1, 1)
    else:
        raise ValueError(f"Unsupported data type: {type(x)}")

if __name__ == "__main__":
    seller_input_raw = {
        "seller_features": 0.87,   # single float
        "product_features": [
            {
                "vision": 0.92,
                "text": 0.81,
                "multimodal": 0.95,
                "ensemble": 0.88,
                "reviews": [0.7, 0.8, 0.9]
            },
            {
                "vision": 0.92,
                "text": 0.81,
                "multimodal": 0.95,
                "ensemble": 0.88,
                "reviews": [0.7, 0.8, 0.9, 0.6, 0.86]
            },
            {
                "vision": 0.92,
                "text": 0.81,
                "multimodal": 0.95,
                "ensemble": 0.88,
                "reviews": [0.7, 0.8, 0.9, 0.92]
            },
        ]
    }

    seller_input = {
        "seller_features": to_tensor(seller_input_raw["seller_features"]),
        "product_features": []
    }

    for p in seller_input_raw["product_features"]:
        seller_input["product_features"].append({
            "vision": to_tensor(p["vision"]),
            "text": to_tensor(p["text"]),
            "multimodal": to_tensor(p["multimodal"]),
            "ensemble": to_tensor(p["ensemble"]),
            "reviews": [to_tensor(r) for r in p["reviews"]],
        })
    
    model = SellerGraphModel(hidden_channels=32)

    risk_score = model(seller_input)
    print(f"Predicted Seller Risk Score: {risk_score.item():.4f}")
