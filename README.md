# AI Resume Analyzer 

A production-level modular AI Resume Analyzer built with Python and Streamlit.

## 🚀 Features

- **Resume Parser**: Extracts text and contact information from PDF resumes.
- **ATS Simulator**: Evaluates resume formatting and compliance with tracking systems.
- **Experience Analyzer**: Analyzes career impact using action verbs and quantifiable metrics.
- **Skill Analyzer**: Categorizes skills into Technical, Soft, and Tools, while detecting buzzwords and outdated tech.
- **Role Match Analyzer**: Uses semantic matching (TF-IDF + Cosine Similarity) to compare resumes against job descriptions.
- **Red Flag Detector**: Identifies gaps, job-hopping, and lack of metrics.
- **Final Scorer**: Aggregates all analyses into a consolidated score and recruiter simulation.

## 🛠️ Project Structure

- `app.py`: Main Streamlit UI.
- `parser.py`: Resume text extraction and structuring.
- `ats.py`: ATS compliance checking logic.
- `experience.py`: Analysis of professional experience impact.
- `skill_analyzer.py`: Skill categorization and matching.
- `role_match.py`: Semantic matching against job descriptions.
- `redflags.py`: Detection of professional red flags.
- `scorer.py`: Aggregation and final scoring.
- `skills_db.py`: Database for skills and keywords.

## 📦 Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 🧪 Testing with Samples

I've included a `sample_generator.py` that creates `sample_resume.pdf` and `sample_job_description.txt` for immediate testing. Run:
```bash
python sample_generator.py
```
Then upload the generated PDF in the app.
