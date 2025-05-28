import streamlit as st
import PyPDF2
import io


def extract_text_from_pdf(file):
	try:
		reader = PyPDF2.PdfReader(file)
		text = ""
		for page in reader.pages:
			text += page.extract_text() + " "
		return text.strip()
	except Exception as e:
		st.error(f"Error reading PDF file: {e}")
		return ""


st.set_page_config(page_title="AI resume/CV reviewer", layout="wide", page_icon="💻")


def simple_job_classifier(resume_text):
	resume_text = resume_text.lower()
	
	job_keywords = {
		"Software Engineer": ["programming", "software", "developer", "java", "python", "c++", "javascript", "react",
		                      "node", "backend", "frontend", "full stack"],
		"Data Scientist": ["data", "machine learning", "ml", "python", "statistics", "r", "deep learning", "analysis",
		                   "tensorflow", "pandas"],
		"Product Manager": ["product management", "roadmap", "stakeholders", "agile", "scrum", "user stories",
		                    "market research"],
		"Graphic Designer": ["photoshop", "illustrator", "design", "creativity", "adobe", "ui", "ux", "graphic"],
		"Marketing Specialist": ["marketing", "seo", "content", "social media", "campaign", "analytics", "branding"],
		"Sales Representative": ["sales", "crm", "leads", "client", "business development", "negotiation"],
		"Human Resources": ["recruitment", "hr", "employee", "training", "talent", "interview", "onboarding"],
		"Finance Analyst": ["finance", "accounting", "budgeting", "financial analysis", "excel", "forecasting",
		                    "audit"],
	}
	
	scores = {job: 0 for job in job_keywords}
	for job, keywords in job_keywords.items():
		for kw in keywords:
			if kw in resume_text:
				scores[job] += 1
	
	# Get job with the highest score
	best_match = max(scores, key=scores.get)
	if scores[best_match] == 0:
		return "No suitable job match found. Please try a more detailed resume."
	return best_match


st.title("AI Resume Reviewer and Job Suggestion Bot")
st.write("Upload your resume (PDF or text), and the bot will suggest a job role that fits your profile.")

uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "txt"])

if uploaded_file:
	file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "file size": uploaded_file.size}
	st.write("File Details:", file_details)
	
	if uploaded_file.type == "application/pdf":
		resume_text = extract_text_from_pdf(uploaded_file)
	else:
		# assume text file
		resume_text = str(uploaded_file.read(), "utf-8")
	
	if resume_text:
		st.subheader("Resume Text Preview:")
		st.write(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))
		
		if st.button("Analyze Resume"):
			with st.spinner("Analyzing your resume..."):
				suggested_job = simple_job_classifier(resume_text)
				st.success(f"Recommended Job Role: **{suggested_job}**")
	else:
		st.warning("Could not extract text from the uploaded resume.")
