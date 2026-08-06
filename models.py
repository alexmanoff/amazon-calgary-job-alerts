from dataclasses import dataclass

@dataclass(frozen=True)
class Job:
    source: str
    job_id: str
    title: str
    location: str
    url: str
    description: str = ""

    @property
    def text(self) -> str:
        return f"{self.title} {self.location} {self.description}".lower()
