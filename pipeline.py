from symptom_extractor import extract_symptoms
from match_engine import match_conditions
from explainer import generate_explanation


def run_triage(user_text):
    symptoms = extract_symptoms(user_text)

    if not symptoms:
        print("No recognizable symptoms found. Please describe your symptoms differently.")
        return

    print(f"Detected symptoms: {symptoms}\n")

    results = match_conditions(symptoms)

    if not results:
        print("No matching conditions found in the database.")
        return

    print("Generating explanation...\n")
    explanation = generate_explanation(symptoms, results)
    print(explanation)


if __name__ == "__main__":
    user_input = "I've had a fever and a really bad cough for two days, feeling super tired too"
    run_triage(user_input)