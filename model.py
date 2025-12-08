from transformers import pipeline

class PhishingModel:
    def __init__(self):
        self.pipe = pipeline("text-classification", model="cybersectony/phishing-email-detection-distilbert_v2.1")

    def predict(self, text):
        # The pipeline returns a list of dictionaries, even for a single input
        result = self.pipe(text)[0]
        label = result['label']
        score = result['score']
        
        # Reverted to original assumption: LABEL_1 is for Phishing
        if label == 'LABEL_1':
            return "Phishing", score
        else:
            return "Safe", score

if __name__ == '__main__':
    # for testing
    model = PhishingModel()
    test_text_phishing = "Urgent action required! Your account has been compromised. Click here to verify your identity."
    test_text_safe = "Hi team, just a reminder about our meeting tomorrow at 10am. Please review the attached agenda."
    
    prediction, confidence = model.predict(test_text_phishing)
    print(f"Text: '{test_text_phishing}'\nPrediction: {prediction}, Confidence: {confidence}\n")

    prediction, confidence = model.predict(test_text_safe)
    print(f"Text: '{test_text_safe}'\nPrediction: {prediction}, Confidence: {confidence}\n")
