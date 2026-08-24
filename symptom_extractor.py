import os
import json
import sqlite3
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_valid_symptoms():
    """Pull the exact list of symptom names from the database."""
    conn = sqlite3.connect('triage.db')
    cursor = conn.cursor()
    cursor.execute("SELECT symptom_name FROM Symptoms")
    symptoms = [row[0] for row in cursor.fetchall()]
    conn.close()
    return symptoms


def extract_symptoms(user_text):
    valid_symptoms = get_valid_symptoms()

    prompt = f"""You are a medical symptom extraction assistant.

Here is the ONLY list of valid symptom names you are allowed to use:
{', '.join(valid_symptoms)}

Read the user's message below and identify which of these EXACT symptoms they are describing.
Only return symptoms from the list above — do not invent new ones.
Return your answer as a JSON array of strings, and nothing else. No explanation, no markdown, just the JSON array.

User's message: "{user_text}"

Example output format: ["Fever", "Cough"]
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # Clean up response in case there's extra formatting
    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        symptoms = json.loads(raw_text)
        return symptoms
    except json.JSONDecodeError:
        print("Warning: Could not parse response:", raw_text)
        return []


# Test it
if __name__ == "__main__":
    user_input = "I've had a fever and a really bad cough for two days, feeling super tired too"
    extracted = extract_symptoms(user_input)
    print(f"User said: {user_input}")
    print(f"Extracted symptoms: {extracted}")