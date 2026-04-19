from skills_db import SKILL_CATEGORIES, BUZZWORDS, OUTDATED_SKILLS

class SkillAnalyzer:
    def __init__(self):
        pass

    def analyze(self, resume_text, jd_text=""):
        found_skills = {cat: [] for cat in SKILL_CATEGORIES}
        found_buzzwords = []
        found_outdated = []
        
        lower_text = resume_text.lower()
        
        # 1. Identify Skills by Category
        for category, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                if skill.lower() in lower_text:
                    found_skills[category].append(skill)

        # 2. Identify Buzzwords
        for word in BUZZWORDS:
            if word.lower() in lower_text:
                found_buzzwords.append(word)

        # 3. Identify Outdated Skills
        for skill in OUTDATED_SKILLS:
            if skill.lower() in lower_text:
                found_outdated.append(skill)

        # 4. Compare with JD
        missing_skills = []
        if jd_text:
            jd_lower = jd_text.lower()
            for category, skills in SKILL_CATEGORIES.items():
                for skill in skills:
                    if skill.lower() in jd_lower and skill.lower() not in lower_text:
                        missing_skills.append(skill)

        # Scoring
        # 10 points per technical skill (up to 50)
        # 5 points per soft skill (up to 25)
        # 5 points per tool (up to 25)
        # Penalty for outdated (-10 each) and buzzwords (-5 each)
        
        tech_score = min(50, len(found_skills['Technical']) * 10)
        soft_score = min(25, len(found_skills['Soft']) * 5)
        tools_score = min(25, len(found_skills['Tools']) * 5)
        
        penalty = (len(found_outdated) * 10) + (len(found_buzzwords) * 2)
        final_score = max(0, min(100, tech_score + soft_score + tools_score - penalty))

        return {
            "score": final_score,
            "found_skills": found_skills,
            "buzzwords": found_buzzwords,
            "outdated": found_outdated,
            "missing": missing_skills
        }
