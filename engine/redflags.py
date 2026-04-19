import re
from datetime import datetime

class RedFlagDetector:
    def __init__(self):
        pass

    def analyze(self, structured_data):
        flags = []
        text = structured_data['raw_text']
        sections = structured_data['sections']
        
        # 1. Employment Gaps & Years Analysis
        # Extract years (e.g., 2018 - 2020)
        years = sorted(list(set(re.findall(r'\b(20\d{2})\b', text))))
        if years:
            years = [int(y) for y in years]
            gaps = []
            for i in range(len(years) - 1):
                if years[i+1] - years[i] > 2: # Significant gap calculation
                    gaps.append(f"{years[i]} to {years[i+1]}")
            
            if gaps:
                flags.append({
                    "type": "Employment Gap",
                    "severity": "Medium",
                    "message": f"Potential gaps detected between: {', '.join(gaps)}",
                    "explanation": "Recruiters often ask about gaps. Ensure you have a valid reason prepared or fill with projects/learning."
                })

        # 2. Job Hopping
        # Rough heuristic: count occurrences of "20xx" in EXPERIENCE
        exp_text = " ".join(sections.get('EXPERIENCE', []))
        dates_in_exp = re.findall(r'\b20\d{2}\b', exp_text)
        if len(dates_in_exp) > 6: # Roughly more than 3 jobs if each has start/end
             flags.append({
                "type": "Job Hopping",
                "severity": "Medium",
                "message": "Multiple short-term stints detected.",
                "explanation": "Frequent job changes can signal instability. Focus on long-term impact in your descriptions."
            })

        # 3. Missing Metrics (Red Flag if almost none)
        bullets = structured_data.get('experience_bullets', [])
        metrics_count = sum(1 for b in bullets if bool(re.search(r'\d+|%|\$', b)))
        if len(bullets) > 0 and (metrics_count / len(bullets)) < 0.2:
            flags.append({
                "type": "Weak Achievements",
                "severity": "High",
                "message": "Lack of quantifiable impact.",
                "explanation": "Your resume describes tasks, not results. Add numbers, percentages, or dollar amounts."
            })

        # 4. Critical Missing Sections
        for section in ['EXPERIENCE', 'EDUCATION']:
            if section not in sections:
                 flags.append({
                    "type": "Incomplete Resume",
                    "severity": "High",
                    "message": f"Missing '{section}' section.",
                    "explanation": "This is a critical section for any professional resume."
                })

        # Calculation of Score
        # Start at 100, deduct based on flags
        score = 100
        for flag in flags:
            if flag['severity'] == "High": score -= 25
            elif flag['severity'] == "Medium": score -= 15
            else: score -= 5
            
        return {
            "score": max(0, score),
            "flags": flags
        }
