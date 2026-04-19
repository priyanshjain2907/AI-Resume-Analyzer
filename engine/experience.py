import re
from skills_db import ACTION_VERBS

class ExperienceAnalyzer:
    def __init__(self):
        self.fluff_phrases = ["responsible for", "tasked with", "handled", "assisted in", "worked on"]

    def analyze(self, bullets):
        role_evaluations = []
        total_impact_score = 0
        
        for bullet in bullets:
            if not bullet.strip(): continue
            
            # 1. Action Verbs
            has_verb = any(v.lower() in bullet.lower() for v in ACTION_VERBS)
            
            # 2. Metrics (Numbers, %, $)
            has_metric = bool(re.search(r'\d+|%|\$', bullet))
            
            # 3. Fluff Detection
            has_fluff = any(f.lower() in bullet.lower() for f in self.fluff_phrases)
            
            # Score this bullet
            bullet_score = 0
            if has_verb: bullet_score += 40
            if has_metric: bullet_score += 60
            if has_fluff: bullet_score -= 20
            
            bullet_score = max(0, min(100, bullet_score))
            total_impact_score += bullet_score
            
            # Generate suggestion if weak
            rewrite = None
            if bullet_score < 70:
                rewrite = f"Action Verb + Quantifiable Result (e.g., 'Developed X reducing latency by 20%')"

            role_evaluations.append({
                "bullet": bullet,
                "score": bullet_score,
                "has_verb": has_verb,
                "has_metric": has_metric,
                "has_fluff": has_fluff,
                "improvement": rewrite
            })

        avg_score = int(total_impact_score / len(bullets)) if bullets else 0
        
        return {
            "score": avg_score,
            "evaluations": role_evaluations,
            "metrics_count": sum(1 for e in role_evaluations if e['has_metric']),
            "verb_count": sum(1 for e in role_evaluations if e['has_verb'])
        }
