from config import LOCATIONS, Profile
from models import Job

def matches(job: Job, profile: Profile) -> tuple[bool, list[str]]:
    text = job.text
    if not any(location in text for location in LOCATIONS):
        return False, []
    if any(word in text for word in profile.exclude):
        return False, []
    reasons = [word for word in profile.include if word in text]
    return bool(reasons), reasons[:4]
