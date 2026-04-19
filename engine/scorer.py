class Scorer:
    def __init__(self):
        # Weights for different dimensions
        self.weights = {
            "ats": 0.25,
            "experience": 0.25,
            "skills": 0.20,
            "role_match": 0.20,
            "red_flags": 0.10
        }

    def calculate_final_score(self, results):
        weighted_score = (
            results['ats']['score'] * self.weights['ats'] +
            results['experience']['score'] * self.weights['experience'] +
            results['skills']['score'] * self.weights['skills'] +
            results['role_match']['score'] * self.weights['role_match'] +
            results['red_flags']['score'] * self.weights['red_flags']
        )
        
        overall_score = int(weighted_score)
        
        # Improvement suggestions aggregation
        improvements = []
        if results['ats']['score'] < 80:
            improvements.append("Improve resume formatting and section headers for better ATS readability.")
        if results['experience']['score'] < 70:
            improvements.append("Strengthen bullet points with more quantifiable metrics and action verbs.")
        if results['skills']['score'] < 60:
            improvements.append("Add missing core technical skills identified from the job description.")
        if results['role_match']['score'] < 50:
            improvements.append("Tailor your summary and experience to better align with the specific job requirements.")
        if len(results['red_flags']['flags']) > 0:
            improvements.append("Address red flags like employment gaps or lack of impact metrics.")

        # Recruiter Simulation
        if overall_score >= 85:
            recruiter_sim = {
                "decision": "Highly Recommended",
                "reasoning": "Strong match with excellent metrics and clear formatting. High probability of interview.",
                "status": "Shortlisted"
            }
        elif overall_score >= 70:
            recruiter_sim = {
                "decision": "Potential Match",
                "reasoning": "Good alignment but needs minor improvements in experience impact or skill coverage.",
                "status": "Under Review"
            }
        else:
            recruiter_sim = {
                "decision": "Needs Significant Work",
                "reasoning": "Fails to meet core alignment or suffers from multiple red flags and weak formatting.",
                "status": "Rejected"
            }

        return {
            "overall_score": overall_score,
            "dimension_scores": {
                "ATS Score": results['ats']['score'],
                "Experience Impact": results['experience']['score'],
                "Skill Strength": results['skills']['score'],
                "Role Alignment": results['role_match']['score'],
                "Professional Integrity": results['red_flags']['score']
            },
            "improvements": improvements,
            "recruiter_simulation": recruiter_sim
        }
