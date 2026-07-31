"""
Prompt templates for LLM Candidate Evaluation and Feedback.
Designed for Llama 3 / Ollama JSON mode.
"""

SYSTEM_PROMPT_EVALUATOR = """
You are an expert Senior Technical Recruiter and Staff Software Engineer at AKM45 Vector AI.
Your task is to analyze candidate resumes against job descriptions and produce detailed, actionable feedback.
Always output strictly valid JSON matching the requested schema.
"""


def build_candidate_analysis_prompt(
    job_title: str,
    job_description: str,
    required_skills: list[str],
    candidate_name: str,
    candidate_resume_text: str,
    matched_skills: list[str],
    missing_skills: list[str],
    ats_score: float,
) -> str:
    return f"""
Analyze the candidate's resume for the position of '{job_title}'.

JOB DETAILS:
- Title: {job_title}
- Required Skills: {', '.join(required_skills)}
- Description: {job_description}

CANDIDATE DETAILS:
- Name: {candidate_name}
- Resume Text: {candidate_resume_text[:3000]}

ATS MATCH SUMMARY:
- Overall Score: {ats_score}/100
- Matched Skills: {', '.join(matched_skills)}
- Missing Skills: {', '.join(missing_skills)}

Return a JSON object with EXACTLY the following structure:
{{
  "candidate_summary": "A 2-3 sentence executive summary of the candidate's background and suitability.",
  "strengths": ["List of 3 key strengths relevant to the job"],
  "weaknesses": ["List of 2 key skill/experience gaps or potential concerns"],
  "missing_critical_skills": ["List of missing skills crucial for this role"],
  "interview_questions": [
    "Question 1 testing candidate's technical experience",
    "Question 2 probing a specific missing skill or project",
    "Question 3 evaluating behavioral / problem solving fit"
  ],
  "hiring_recommendation": "Strong Hire" | "Hire" | "Possible Fit" | "Do Not Pursue",
  "recommendation_reasoning": "1 sentence explanation for the hiring recommendation."
}}
"""
