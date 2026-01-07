from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

@dataclass
class ResumeAnalysis:
    filename: str
    filepath: str
    skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    match_score: float
    similarity_score: float
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict:
        return self.__dict__
