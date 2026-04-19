import re
import io
from pdfminer.high_level import extract_text

class ResumeParser:
    def __init__(self):
        self.sections = [
            'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 
            'CERTIFICATIONS', 'SUMMARY', 'AWARDS', 'LANGUAGES'
        ]

    def extract_text(self, pdf_file):
        """Extract text from a PDF file-like object."""
        try:
            text = extract_text(pdf_file)
            return text
        except Exception as e:
            print(f"Error extracting text: {e}")
            return ""

    def extract_contact_info(self, text):
        """Extract contact details using regex."""
        email = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        phone = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        linkedin = re.findall(r'linkedin\.com/in/[\w\d-]+', text)
        github = re.findall(r'github\.com/[\w\d-]+', text)
        
        # Simple name extraction (usually first line)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        name = lines[0] if lines else "Unknown"

        return {
            "name": name,
            "email": email[0] if email else None,
            "phone": phone[0] if phone else None,
            "linkedin": linkedin[0] if linkedin else None,
            "github": github[0] if github else None
        }

    def parse(self, text):
        """Structure extracted text into sections."""
        structured_data = {
            "contact": self.extract_contact_info(text),
            "sections": {},
            "raw_text": text,
            "metadata": {
                "word_count": len(text.split()),
                "page_estimate": max(1, len(text) // 3000) # Rough estimate
            }
        }

        # Identify sections
        lines = text.split('\n')
        current_section = "General"
        structured_data["sections"][current_section] = []

        for line in lines:
            clean_line = line.strip()
            if not clean_line:
                continue
            
            # Check if line is a section header (all caps, or matches known list)
            is_header = False
            upper_line = clean_line.upper().replace(':', '')
            if upper_line in self.sections:
                current_section = upper_line
                if current_section not in structured_data["sections"]:
                    structured_data["sections"][current_section] = []
                is_header = True
            
            if not is_header:
                structured_data["sections"][current_section].append(clean_line)

        # Process experience specifically for bullets
        exp_text = structured_data["sections"].get("EXPERIENCE", [])
        structured_data["experience_bullets"] = [line for line in exp_text if line.startswith(('•', '-', '*')) or len(line.split()) > 5]

        return structured_data

if __name__ == "__main__":
    # Test with dummy text
    parser = ResumeParser()
    dummy_text = "John Doe\njohn@example.com\nEXPERIENCE\n• Led a team of 5 to build a website.\nSKILLS\nPython, React"
    print(parser.parse(dummy_text))
