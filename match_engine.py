import sqlite3

def match_conditions(reported_symptoms):
    conn = sqlite3.connect('triage.db')
    cursor = conn.cursor()

    # Create placeholders like ?,?,? based on how many symptoms were reported
    placeholders = ','.join('?' for _ in reported_symptoms)

    query = f"""
        SELECT c.condition_name, c.base_urgency_level, SUM(sc.weight) AS total_score
        FROM Symptom_Condition sc
        JOIN Symptoms s ON sc.symptom_id = s.symptom_id
        JOIN Conditions c ON sc.condition_id = c.condition_id
        WHERE s.symptom_name IN ({placeholders})
        GROUP BY c.condition_id
        ORDER BY total_score DESC
    """

    cursor.execute(query, reported_symptoms)
    results = cursor.fetchall()
    conn.close()
    return results


# Test it
user_symptoms = ['Chest Pain', 'Shortness of Breath']
matches = match_conditions(user_symptoms)

print(f"Based on symptoms {user_symptoms}, possible conditions:")
for condition_name, urgency, score in matches:
    print(f"  - {condition_name} (urgency: {urgency}) — score: {score}")