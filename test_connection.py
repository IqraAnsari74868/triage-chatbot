import sqlite3

# Connect to the database (same folder as this script)
conn = sqlite3.connect('triage.db')
cursor = conn.cursor()

# Test query: find all conditions linked to 'Fever', sorted by likelihood
cursor.execute("""
    SELECT c.condition_name, sc.weight
    FROM Symptom_Condition sc
    JOIN Symptoms s ON sc.symptom_id = s.symptom_id
    JOIN Conditions c ON sc.condition_id = c.condition_id
    WHERE s.symptom_name = 'Fever'
    ORDER BY sc.weight DESC
""")

results = cursor.fetchall()

print("Conditions linked to Fever:")
for condition_name, weight in results:
    print(f"  - {condition_name}: {weight}")

conn.close()