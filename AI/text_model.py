from transformers import pipeline

class TextModel:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def predict(self, title: str, desc: str) -> float:
        text = f"{title}. {desc}"
        result = self.classifier(text)[0]
        if result['label'] == 'POSITIVE':
            return float(result['score'])
        else:
            return 1 - float(result['score'])