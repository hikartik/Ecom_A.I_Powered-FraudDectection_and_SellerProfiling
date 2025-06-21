from transformers import pipeline

class ReviewBehaviorScorer:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="joeddav/distilbert-base-uncased-go-emotions-student")


    def score_reviews(self, reviews):
        scores = []
        for review in reviews:
            result = self.classifier(review)[0]
            label = result['label']
            score = result['score']
            if label.lower() in ['fake', 'unreliable', 'false']:
                scores.append(1 - score)  # less credible
            else:
                scores.append(score)      # more credible
        return scores