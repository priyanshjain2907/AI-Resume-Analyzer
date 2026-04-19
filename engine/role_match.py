from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class RoleMatchAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def analyze(self, resume_text, jd_text):
        if not jd_text or not resume_text:
            return {"score": 0, "match_percentage": "0%", "matched_keywords": [], "explanation": "Provide both resume and JD for analysis."}
        
        # Preprocessing: Basic cleaning
        texts = [resume_text, jd_text]
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Extract important keywords from JD
            feature_names = self.vectorizer.get_feature_names_out()
            jd_vector = tfidf_matrix[1:2].toarray()[0]
            
            # Get top 10 keywords by TF-IDF score in JD
            top_indices = jd_vector.argsort()[-15:][::-1]
            top_keywords = [feature_names[i] for i in top_indices if jd_vector[i] > 0]
            
            # Check which of these are in the resume
            matched_keywords = [word for word in top_keywords if word.lower() in resume_text.lower()]
            
            match_score = int(similarity * 100)
            
            return {
                "score": match_score,
                "match_percentage": f"{match_score}%",
                "matched_keywords": matched_keywords,
                "missing_keywords": [w for w in top_keywords if w not in matched_keywords],
                "explanation": f"The resume has a {match_score}% semantic alignment with the role requirements."
            }
        except Exception as e:
            return {"score": 0, "error": str(e), "explanation": "Error during semantic analysis."}
