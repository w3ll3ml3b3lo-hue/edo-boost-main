import json
import uuid
import random

subjects = {
    "MATH": {"concepts": ["addition", "subtraction", "multiplication", "division", "fractions", "geometry"]},
    "ENG": {"concepts": ["vocabulary", "grammar", "comprehension", "spelling", "phonics"]}
}

sql = "BEGIN;\n\nINSERT INTO item_bank (item_id, subject_code, grade_level, concept_code, difficulty, discrimination, guessing, content, options, correct_answer, is_active) VALUES\n"

values = []
for subject_code, data in subjects.items():
    for grade in range(1, 6):  # Grades 1 to 5
        for _ in range(10):    # 10 items per grade per subject = 50 per subject
            item_id = str(uuid.uuid4())
            concept = random.choice(data["concepts"])
            diff = round(random.uniform(-2.5, 2.5), 2)
            discrim = round(random.uniform(0.5, 2.5), 2)
            guess = round(random.uniform(0.1, 0.25), 2)
            
            content = f"What is the correct answer for {concept} (Grade {grade})?"
            options = json.dumps(["Option A", "Option B", "Option C", "Option D"])
            correct = random.choice(["Option A", "Option B", "Option C", "Option D"])
            
            val = f"('{item_id}', '{subject_code}', {grade}, '{concept}', {diff}, {discrim}, {guess}, '{content}', '{options}'::jsonb, '{correct}', TRUE)"
            values.append(val)

sql += ",\n".join(values) + "\nON CONFLICT DO NOTHING;\n\nCOMMIT;\n"

with open("/home/nkgolol/Dev/SandBox/edo-boost-main/edo-boost-main/scripts/db_seed_items.sql", "w") as f:
    f.write(sql)
print("Generated 100 items in scripts/db_seed_items.sql")
