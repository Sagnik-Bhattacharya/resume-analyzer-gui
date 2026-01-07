import os

ALLOWED_EXTENSIONS = {".pdf", ".docx"}

def is_valid_resume(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path.lower())
    return ext in ALLOWED_EXTENSIONS
