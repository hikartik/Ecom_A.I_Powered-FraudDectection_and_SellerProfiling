try:
    from transformers import pipeline
except Exception:  # pragma: no cover - transformers may be unavailable
    pipeline = None


class TextModel:
    def __init__(self):
        """Sentiment model with an offline fallback."""
        if pipeline is not None:
            try:
                self.classifier = pipeline(
                    "text-classification",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                )
            except Exception:
                self.classifier = None
        else:
            self.classifier = None

    def predict(self, title: str, desc: str) -> float:
        text = f"{title}. {desc}".lower()
        if self.classifier is None:
            positive_words = {"great", "excellent", "amazing", "recommend"}
            negative_words = {"worst", "bad", "terrible"}
            if any(w in text for w in positive_words):
                return 0.9
            if any(w in text for w in negative_words):
                return 0.1
            return 0.5

        result = self.classifier(text)[0]
        if result["label"] == "POSITIVE":
            return float(result["score"])
        else:
            return 1 - float(result["score"])
