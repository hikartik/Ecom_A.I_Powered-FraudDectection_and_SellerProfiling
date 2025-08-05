try:
    from transformers import pipeline
except Exception:  # pragma: no cover - transformers may be unavailable
    pipeline = None

class ReviewBehaviorScorer:
    def __init__(self):
        if pipeline is not None:
            try:
                self.classifier = pipeline(
                    "text-classification",
                    model="joeddav/distilbert-base-uncased-go-emotions-student",
                )
            except Exception:
                self.classifier = None
        else:
            self.classifier = None


    def score_reviews(self, reviews):
        scores = []
        for review in reviews:
            if self.classifier is None:
                negative_words = {"worst", "bad", "terrible", "fake"}
                positive_words = {"great", "excellent", "amazing"}
                text = review.lower()
                if any(w in text for w in negative_words):
                    scores.append(0.2)
                elif any(w in text for w in positive_words):
                    scores.append(0.8)
                else:
                    scores.append(0.5)
                continue

            result = self.classifier(review)[0]
            label = result['label']
            score = result['score']
            if label.lower() in ['fake', 'unreliable', 'false']:
                scores.append(1 - score)  # less credible
            else:
                scores.append(score)      # more credible
        return scores