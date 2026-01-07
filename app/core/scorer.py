def score_resume(resume_skills: list, job_skills: list) -> dict:
    resume_set = set(map(str.lower, resume_skills))
    job_set = set(map(str.lower, job_skills))

    matched = resume_set & job_set
    missing = job_set - resume_set

    score = round((len(matched) / max(len(job_set), 1)) * 100, 2)

    return {
        "score": score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
    }
