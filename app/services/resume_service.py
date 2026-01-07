from app.models.resume import ResumeAnalysis
from app.repositories.resume_repo import ResumeRepository

class ResumeService:
    def __init__(self):
        self.repo = ResumeRepository()

    def save_analysis(
        self,
        filename,
        skills,
        filepath,
        score_data,
        similarity
    ):
        resume = ResumeAnalysis(
            filename=filename,
            filepath = str(filepath),
            skills=skills,
            matched_skills=score_data["matched_skills"],
            missing_skills=score_data["missing_skills"],
            match_score=score_data["score"],
            similarity_score=similarity
        )
        self.repo.save(resume.to_dict())
    
    def get_all_resumes(self):
            return self.repo.get_all_resumes()