from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    due_time: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    completed: bool = False
    priority_value: int = field(init=False)

    def __post_init__(self):
        pass

    def mark_complete(self):
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def list_tasks(self) -> list:
        pass

    def pending_tasks(self) -> list:
        pass


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def list_pets(self) -> list:
        pass


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int = 480, start_time: str = "9:00 AM"):
        self.owner = owner
        self.available_minutes = available_minutes
        self.start_time = start_time
        self.schedule: list[dict] = []

    def get_all_tasks(self) -> list:
        pass

    def build_schedule(self):
        pass

    def filter_by_priority(self, min_priority: str) -> list:
        pass

    def explain_plan(self) -> list:
        pass
