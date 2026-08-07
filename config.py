from dataclasses import dataclass

@dataclass(frozen=True)
class Profile:
    name: str
    chat_id_env: str
    include: tuple[str, ...]
    exclude: tuple[str, ...]

LOCATIONS = ("calgary", "rocky view", "rocky view county", "balzac")

ALEX = Profile(
    "Alex",
    "ALEX_CHAT_ID",
    ("warehouse", "fulfillment", "fulfilment", "sortation", "delivery station",
     "package handler", "seasonal associate", "locker associate"),
    ("driver", "area manager", "operations manager", "maintenance technician",
     "software engineer", "xl warehouse"),
)

MOM = Profile(
    "Mom",
    "MOM_CHAT_ID",
    ("project manager", "program manager", "project coordinator",
     "program coordinator", "operations manager", "operations coordinator",
     "transportation", "logistics coordinator", "fleet coordinator",
     "safety coordinator", "compliance coordinator", "process improvement",
     "continuous improvement", "implementation manager", "site lead",
     "driver trainer", "dispatch coordinator", "business operations"),
    ("software engineer", "data scientist", "maintenance technician"),
)

PROFILES = (ALEX,)
