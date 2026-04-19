from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_sample_resume():
    c = canvas.Canvas("sample_resume.pdf", pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "John Developer")
    
    # Contact
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, "john.developer@email.com | (555) 123-4567")
    c.drawString(50, height - 85, "linkedin.com/in/johndev | github.com/johndev")
    
    # Summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "SUMMARY")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 140, "Senior Python Developer with 5+ years of experience in building scalable web applications.")
    
    # Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 170, "EXPERIENCE")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 190, "Tech Solutions Inc. - Senior Developer (2018 - Present)")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 205, "- Led a team of 10 developers to build a microservices architecture using FastAPI.")
    c.drawString(50, height - 220, "- Improved system performance by 40% through Redis caching and SQL optimization.")
    c.drawString(50, height - 235, "- Integrated CI/CD pipelines reducing deployment time by 50%.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 265, "Data Corp - Software Engineer (2015 - 2018)")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 280, "- Developed data processing pipelines using Python and Pandas.")
    c.drawString(50, height - 295, "- Managed PostgreSQL databases with over 1TB of data.")
    c.drawString(50, height - 310, "- Collaborated with cross-functional teams to deliver projects on time.")
    
    # Skills
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 340, "SKILLS")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 360, "Technical: Python, FastAPI, Django, PostgreSQL, Redis, Docker, AWS")
    c.drawString(50, height - 375, "Tools: Git, Jenkins, Jira, Slack")
    
    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 405, "EDUCATION")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 425, "B.S. in Computer Science - University of Technology (2011 - 2015)")
    
    c.save()
    print("Sample resume 'sample_resume.pdf' created successfully.")

def create_sample_jd():
    jd = """
    Job Title: Senior Python Backend Engineer
    Location: Remote
    
    About the Role:
    We are looking for a Senior Python Developer to join our core team. You will be responsible for building high-performance APIs and managing scalable data systems.
    
    Requirements:
    - 5+ years of experience with Python (FastAPI or Django).
    - Strong experience with SQL (PostgreSQL) and NoSQL (Redis).
    - Deep understanding of Docker and Kubernetes.
    - Experience with AWS services (EC2, S3, RDS).
    - Knowledge of CI/CD practices and Git.
    - Ability to lead teams and mentor junior developers.
    
    Bonus Skills:
    - Experience with Rust or Go.
    - Knowledge of Machine Learning pipelines.
    """
    with open("sample_job_description.txt", "w") as f:
        f.write(jd)
    print("Sample JD 'sample_job_description.txt' created successfully.")

if __name__ == "__main__":
    create_sample_resume()
    create_sample_jd()
