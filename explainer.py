import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_explanation(user_symptoms, results):
    # Format the top 3 results for the prompt
    conditions_text = "\n".join(
        [f"- {name} (urgency: {urgency}, match score: {score:.2f})"
         for name, urgency, score in results[:3]]
    )

    prompt = f"""You are a calm, clear medical triage assistant. You are NOT a doctor and must never claim to diagnose.

The user reported these symptoms: {', '.join(user_symptoms)}

Based on a symptom-matching database, here are the top possible conditions:
{conditions_text}

Write a short, plain-language response (4-6 sentences) that:
1. Briefly explains why these conditions match their symptoms
2. Clearly states the urgency level and what they should do next
3. Ends with this exact disclaimer: "This is an educational tool, not a medical diagnosis. Please consult a healthcare professional for accurate advice."

Keep the tone calm and clear, not alarming, even for high-urgency results.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text


if __name__ == "__main__":
    # Quick test with dummy data
    test_symptoms = ['Chest Pain', 'Shortness of Breath']
    test_results = [
        ('Heart Attack', 'Seek care now', 1.7),
        ('Angina', 'High', 1.4),
        ('Pneumonia', 'High', 0.8)
    ]
    explanation = generate_explanation(test_symptoms, test_results)
    print(explanation)