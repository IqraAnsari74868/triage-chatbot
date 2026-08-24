# 🩺 Triage Chatbot

An AI-powered symptom-checker tool that takes free-text symptom descriptions and returns possible conditions with urgency levels — combining a **SQL database**, **Python matching logic**, and **LLM prompt engineering**.

> ⚠️ Educational project only. Not a medical device and not a substitute for professional medical advice.

---

## Live Demo

![Triage Chatbot Screenshot](screenshot.png)
*(Add your screenshot here — see "Adding a Screenshot" below)*

---

## What This Project Proves

> I can build a symptom-checker tool that takes user-input symptoms and returns possible conditions with urgency levels, by combining a SQL database (structured symptom-condition data), Python (matching logic), and LLM prompt engineering (plain-language explanations and safety handling).

This project was built end-to-end — schema design, matching logic, LLM integration, and UI — as a demonstration of practical AI + data engineering skills.

---

## How It Works

1. **User types symptoms in plain English** (e.g., *"I've had a fever and a bad cough for two days, feeling really tired"*)
2. **Gemini API extracts structured symptoms**, grounded against the exact symptom list in the database (prevents hallucinated symptom names)
3. **SQL matching engine** joins `Symptoms → Symptom_Condition → Conditions`, using `GROUP BY` and `SUM()` to rank conditions by combined likelihood score
4. **Gemini API generates a plain-language explanation**, referencing the matched conditions, their urgency levels, and a safety disclaimer
5. **Streamlit UI** displays detected symptoms, color-coded urgency cards, and the explanation

```
User input (free text)
      │
      ▼
[Gemini] Symptom Extraction  →  structured symptom list
      │
      ▼
[SQLite] Matching Engine (JOIN + GROUP BY + SUM)  →  ranked conditions
      │
      ▼
[Gemini] Explanation Generator  →  plain-language, urgency-aware summary
      │
      ▼
[Streamlit] UI displays results
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Database | SQLite |
| Backend logic | Python |
| AI / NLP | Google Gemini API (prompt engineering) |
| UI | Streamlit |

---

## Database Schema

Six tables, normalized to separate fixed reference data from per-session data:

| Table | Purpose |
|---|---|
| `Symptoms` | Master list of symptoms |
| `Conditions` | Master list of conditions + base urgency level |
| `Symptom_Condition` | Many-to-many link table with likelihood weight |
| `Follow_Up_Questions` | Question bank (including general medical history questions) |
| `Sessions` | Anonymous conversation anchor (ID + timestamp, no user accounts) |
| `Session_Symptoms` | Reported symptom details per session (severity, onset, location) |

No user accounts or authentication are used — sessions are anonymous and ephemeral by design (see Scope below).

---

## Project Scope

Defined before development began, to keep the MVP focused and avoid scope creep.

### In Scope (MVP)
- Free-text symptom input (not checkboxes — exercises the LLM/NLP layer)
- Follow-up clarifying question bank for ambiguous input
- SQL database of symptoms, conditions, and their relationships
- Python logic to query and rank possible conditions
- LLM-generated explanation of *why* each condition matched
- Urgency level output (Low / Medium / High / Seek care now)
- Clear educational-use disclaimer on every result

### Out of Scope / Future Work

| Feature | Reason Excluded |
|---|---|
| User accounts / login | Not needed to prove the core skillset; adds unnecessary complexity |
| Multi-language support | Doesn't demonstrate core skills; scope creep |
| Persistent symptom history | Depends on user authentication, which is intentionally excluded |
| Real hospital/appointment API integration | Too complex for MVP scope; noted for future work |
| Polished UI | Valuable, but a presentation-layer concern — built after core logic was working |

### Success Criteria
- User can type symptoms in plain English
- System asks relevant follow-up questions when needed
- Returns 1–3 ranked possible conditions from the database
- Each result includes a plain-language explanation of the match
- Each result includes an urgency level
- Disclaimer shown with every result

---

## Setup / Run Locally

```bash
# Clone the repo
git clone https://github.com/IqraAnsari74868/triage-chatbot.git
cd triage-chatbot

# Install dependencies
pip install streamlit google-genai python-dotenv

# Add your own Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the app
python -m streamlit run app.py
```

Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/).

---

## Project Structure

```
triage-chatbot/
├── app.py                  # Streamlit UI
├── symptom_extractor.py    # Free-text → structured symptoms (Gemini)
├── match_engine.py         # SQL matching + ranking logic
├── explainer.py            # Plain-language explanation generation (Gemini)
├── pipeline.py             # CLI version tying all steps together
├── triage.db                # SQLite database
└── .gitignore
```

---

## What I Learned

- Designing a normalized relational schema, including many-to-many relationships with weighted scoring
- Writing parameterized SQL queries (`?` placeholders) to safely handle dynamic input and prevent SQL injection
- Prompt engineering techniques for grounding LLM output against a fixed reference list, to avoid hallucination
- Structuring an LLM pipeline: extraction → business logic → explanation, rather than relying on the LLM for everything
- Defining project scope deliberately before writing code, and recognizing when a "nice" feature secretly depends on something already excluded (e.g., symptom history requiring user accounts)

---

## Disclaimer

This tool is for educational and portfolio purposes only. It is not a medical device, does not provide medical advice, and should never be used as a substitute for consultation with a qualified healthcare professional.
