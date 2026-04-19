import streamlit as st
import plotly.graph_objects as go
from parser import ResumeParser
from ats import ATSSimulator
from experience import ExperienceAnalyzer
from skill_analyzer import SkillAnalyzer
from role_match import RoleMatchAnalyzer
from redflags import RedFlagDetector
from scorer import Scorer

# --- Page Config ---
st.set_page_config(
    page_title="AI Resume Analyzer Pro",
    page_icon="🤖",
    layout="wide"
)

# --- Styling ---
st.markdown("""
<style>
.main { background-color: #0e1117; }
.stMetric {
    background-color: #1e2130;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #3e4149;
}
</style>
""", unsafe_allow_html=True)

# --- Initialize Modules ---
parser = ResumeParser()
ats_sim = ATSSimulator()
exp_analyzer = ExperienceAnalyzer()
skill_analyzer = SkillAnalyzer()
role_matcher = RoleMatchAnalyzer()
red_flag_detector = RedFlagDetector()
scorer = Scorer()

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    jd_text = st.text_area("Job Description", height=250)
    analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True)

# --- Main ---
st.title("🤖 AI Resume Analyzer Pro")

if analyze_btn and uploaded_file:

    with st.spinner("Analyzing..."):

        # Parsing
        raw_text = parser.extract_text(uploaded_file)
        structured_data = parser.parse(raw_text)

        # Analysis
        ats_results = ats_sim.analyze(structured_data, jd_text)
        exp_results = exp_analyzer.analyze(structured_data.get('experience_bullets', []))
        skill_results = skill_analyzer.analyze(raw_text, jd_text)
        role_results = role_matcher.analyze(raw_text, jd_text)
        flag_results = red_flag_detector.analyze(structured_data)

        # Final Score
        all_results = {
            "ats": ats_results,
            "experience": exp_results,
            "skills": skill_results,
            "role_match": role_results,
            "red_flags": flag_results
        }

        final_analysis = scorer.calculate_final_score(all_results)

        # ---------------- TOP SECTION ----------------

        st.markdown("## Analysis Complete")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("ATS Score", f"{ats_results['score']}%")
        col2.metric("Experience", f"{exp_results['score']}%")
        col3.metric("Skills", f"{skill_results['score']}%")
        col4.metric("Role Match", f"{role_results['score']}%")

        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=final_analysis['overall_score'],
            title={'text': "Overall Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#00c3ff"},
                'steps': [
                    {'range': [0, 50], 'color': '#ff5252'},
                    {'range': [50, 75], 'color': '#ffd600'},
                    {'range': [75, 100], 'color': '#00c853'}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # ---------------- SECTIONS ----------------

        st.markdown("## 📊 Analysis Sections")

        # ATS
        with st.expander("🤖 ATS Simulation"):
            st.write(f"Score: {ats_results['score']}%")
            for check in ats_results['checks']:
                st.write(f"{check['name']} → {check['message']}")

        # Experience
        with st.expander("💼 Experience Deep Evaluation"):
            st.write(f"Impact Score: {exp_results['score']}%")
            for eval in exp_results['evaluations'][:5]:
                st.write(eval['bullet'])
                if eval['improvement']:
                    st.info(eval['improvement'])

        # Skills
        with st.expander("🛠️ Skill Intelligence"):
            for cat, skills in skill_results['found_skills'].items():
                if skills:
                    st.write(f"{cat}: {', '.join(skills)}")

            st.write("Match:", role_results['matched_keywords'])

            if skill_results['missing']:
                st.error(f"Missing: {', '.join(skill_results['missing'])}")

        # Red Flags
        with st.expander("🚩 Red Flags"):
            if not flag_results['flags']:
                st.success("No issues")
            else:
                for flag in flag_results['flags']:
                    st.error(flag['message'])

        # Improvements
        with st.expander("🚀 Improvements"):
            for imp in final_analysis['improvements']:
                st.info(imp)

else:
    st.info("Upload resume and click Analyze")