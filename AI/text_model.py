from transformers import pipeline

class TextModel:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="bert-base-uncased", top_k=None)

    def predict(self, text):
        result = self.classifier(text)[0]
        return float(result['score']) if result['label'] == 'LABEL_1' else 1 - float(result['score'])
