from dataclasses import dataclass, field


@dataclass
class Pet:
    name: str
    species: str


@dataclass
class Owner:
    name: str
    pet: Pet


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    priority_value: int = field(init=False)

    def __post_init__(self):
        mapping = {"low": 1, "medium": 2, "high": 3}
        self.priority_value = mapping.get(self.priority, 0)


class Scheduler:
    def __init__(self, owner: Owner, tasks: list[Task], available_minutes: int = 480):
        self.owner = owner
        self.tasks = tasks
        self.available_minutes = available_minutes
        self.schedule: list[dict] = []

    def build_schedule(self):
        # TODO: sort tasks by priority_value, fit within available_minutes
        pass

    def explain_plan(self) -> list[str]:
        # TODO: format each item in self.schedule into a readable string
        pass
