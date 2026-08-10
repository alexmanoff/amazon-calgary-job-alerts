from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    chat_id_env: str
    include: tuple[str, ...]
    exclude: tuple[str, ...]


LOCATIONS = (
    "calgary",
    "rocky view",
    "rocky view county",
    "balzac",
    "airdrie",
)

ALEX = Profile(
    "Alex",
    "ALEX_CHAT_ID",
    (
        "warehouse",
        "warehouse associate",
        "fulfillment",
        "fulfilment",
        "fulfillment associate",
        "fulfilment associate",
        "sortation",
        "sortation associate",
        "delivery station",
        "delivery station associate",
        "package handler",
        "seasonal associate",
        "locker associate",
        "operations associate",
        "logistics associate",
        "material handler",
        "inventory associate",
        "distribution associate",
        "shipping associate",
        "receiving associate",
        "order picker",
        "picker packer",
        "picker/packer",
    ),
    (
        "driver",
        "manager",
        "engineer",
        "specialist",
        "technician",
        "architect",
        "scientist",
        "analyst",
        "developer",
        "consultant",
        "supervisor",
        "lead ",
        "senior",
        "sr.",
        "principal",
        "intern",
        "maintenance",
        "xl warehouse",
    ),
)

MOM = Profile(
    "Mom",
    "MOM_CHAT_ID",
    (
        "project manager",
        "program manager",
        "project coordinator",
        "program coordinator",
        "operations manager",
        "operations coordinator",
        "transportation",
        "logistics coordinator",
        "fleet coordinator",
        "safety coordinator",
        "compliance coordinator",
        "process improvement",
        "continuous improvement",
        "implementation manager",
        "site lead",
        "driver trainer",
        "dispatch coordinator",
        "business operations",
    ),
    (
        "software engineer",
        "data scientist",
        "maintenance technician",
    ),
)

# Mom stays disabled until Alex's profile and delivery flow are fully validated.
PROFILES = (ALEX,)
