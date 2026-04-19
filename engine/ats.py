import re
from skills_db import ACTION_VERBS

class ATSSimulator:
    def __init__(self):
        self.mandatory_sections = ['EXPERIENCE', 'EDUCATION', 'SKILLS']
        
    def analyze(self, structured_data, jd_text=""):
        checks = []
        score = 0
        total_checks = 7

        # 1. Section Presence
        missing_sections = [s for s in self.mandatory_sections if s not in structured_data['sections']]
        if not missing_sections:
            checks.append({"name": "Section Presence", "status": "pass", "message": "All essential sections found."})
            score += 1
        else:
            checks.append({"name": "Section Presence", "status": "fail", "message": f"Missing sections: {', '.join(missing_sections)}"})

        # 2. Contact Info
        contact = structured_data['contact']
        if contact['email'] and contact['phone']:
            checks.append({"name": "Contact Information", "status": "pass", "message": "Email and Phone found."})
            score += 1
        else:
            checks.append({"name": "Contact Information", "status": "warn", "message": "Email or Phone missing."})
            score += 0.5

        # 3. Resume Length
        pages = structured_data['metadata']['page_estimate']
        if 1 <= pages <= 2:
            checks.append({"name": "Resume Length", "status": "pass", "message": f"Optimal length ({pages} page(s))."})
            score += 1
        else:
            checks.append({"name": "Resume Length", "status": "warn", "message": f"Length is {pages} page(s). 1-2 is ideal."})
            score += 0.5

        # 4. Action Verbs
        bullets = structured_data.get('experience_bullets', [])
        found_verbs = [v for v in ACTION_VERBS if any(v.lower() in b.lower() for b in bullets)]
        if len(found_verbs) >= 5:
            checks.append({"name": "Action Verbs", "status": "pass", "message": f"Strong usage of action verbs ({len(found_verbs)} found)."})
            score += 1
        else:
            checks.append({"name": "Action Verbs", "status": "fail", "message": "Weak action verb usage. Use words like 'Led', 'Developed', 'Managed'."})

        # 5. Bullet Points
        if len(bullets) >= 5:
            checks.append({"name": "Bullet Consistency", "status": "pass", "message": f"Good amount of detailed bullets ({len(bullets)} total)."})
            score += 1
        else:
            checks.append({"name": "Bullet Consistency", "status": "warn", "message": "Too few bullet points or descriptions."})
            score += 0.5

        # 6. Keyword Coverage (Simple)
        if jd_text:
            jd_words = set(re.findall(r'\w+', jd_text.lower()))
            resume_words = set(re.findall(r'\w+', structured_data['raw_text'].lower()))
            common = jd_words.intersection(resume_words)
            important_keywords = [w for w in common if len(w) > 3] # Filter small words
            
            coverage = len(important_keywords) / len(jd_words) if jd_words else 0
            if coverage > 0.3:
                checks.append({"name": "Keyword Coverage", "status": "pass", "message": f"Good alignment with Job Description."})
                score += 1
            else:
                checks.append({"name": "Keyword Coverage", "status": "warn", "message": "Low keyword match with Job Description."})
                score += 0.5
        else:
            checks.append({"name": "Keyword Coverage", "status": "skip", "message": "No Job Description provided for matching."})
            total_checks -= 1

        # 7. Metrics Presence (%)
        metrics = [b for b in bullets if '%' in b or any(char.isdigit() for char in b)]
        if len(metrics) >= 3:
            checks.append({"name": "Quantitative Metrics", "status": "pass", "message": "Strong use of numbers and data."})
            score += 1
        else:
            checks.append({"name": "Quantitative Metrics", "status": "warn", "message": "Add more metrics (e.g., % increase, revenue, team size)."})
            score += 0.5

        final_score = int((score / total_checks) * 100)
        
        return {
            "score": final_score,
            "pass": final_score >= 70,
            "checks": checks,
            "rejection_reasons": [c['message'] for c in checks if c['status'] == 'fail']
        }
