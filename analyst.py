from google import genai

class PhishingAnalyst:
    def __init__(self, api_key):
        
        self.client = genai.Client(api_key=api_key)

        self.model_id = "gemini-2.5-flash"

    def analyze_threat(self, email_text):
        prompt = f"""
        Act as a Cyber Security Analyst. Analyze the following email for phishing indicators. 
        Provide a concise 3-bullet point summary explaining why it is or isn't a threat.
        Use a user-friendly layout for output.
        
        Email: {email_text}
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text