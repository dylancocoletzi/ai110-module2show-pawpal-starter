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
        """Map priority string to a numeric value for sorting."""
        mapping = {"low": 1, "medium": 2, "high": 3}
        self.priority_value = mapping.get(self.priority, 0)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def list_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks

    def pending_tasks(self) -> list:
        """Return only tasks that have not been completed."""
        return [t for t in self.tasks if not t.completed]


@dataclass
class Owner:
    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def list_pets(self) -> list:
        """Return all pets belonging to this owner."""
        return self.pets


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int = 480, start_time: str = "9:00 AM"):
        self.owner = owner
        self.available_minutes = available_minutes
        self.start_time = start_time
        self.schedule: list[dict] = []

    def get_all_tasks(self) -> list:
        """Aggregate pending tasks across all of the owner's pets as (pet, task) tuples."""
        all_tasks = []
        for pet in self.owner.pets:
            for task in pet.pending_tasks():
                all_tasks.append((pet, task))
        return all_tasks

    def build_schedule(self):
        """Sort tasks by priority and fit them into the available time budget."""
        self.schedule = []
        all_tasks = self.get_all_tasks()
        sorted_tasks = sorted(all_tasks, key=lambda x: x[1].priority_value, reverse=True)

        minutes_used = 0
        start_hour, start_minute = self._parse_time(self.start_time)

        for pet, task in sorted_tasks:
            if minutes_used + task.duration_minutes > self.available_minutes:
                continue
            task_start = self._format_time(start_hour, start_minute + minutes_used)
            self.schedule.append({
                "pet": pet.name,
                "task": task.title,
                "start_time": task_start,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "due_time": task.due_time,
            })
            minutes_used += task.duration_minutes

    def _parse_time(self, time_str: str):
        """Convert a time string like '9:00 AM' into (hour, minute) integers."""
        time_part, period = time_str.split(" ")
        hour, minute = map(int, time_part.split(":"))
        if period == "PM" and hour != 12:
            hour += 12
        return hour, minute

    def _format_time(self, hour: int, minute: int) -> str:
        """Convert (hour, minute) integers back into a readable time string."""
        hour += minute // 60
        minute = minute % 60
        period = "AM" if hour < 12 else "PM"
        display_hour = hour if hour <= 12 else hour - 12
        if display_hour == 0:
            display_hour = 12
        return f"{display_hour}:{minute:02d} {period}"

    def filter_by_priority(self, min_priority: str) -> list:
        """Return only tasks at or above the given minimum priority level."""
        min_value = {"low": 1, "medium": 2, "high": 3}.get(min_priority, 1)
        return [
            (pet, task) for pet, task in self.get_all_tasks()
            if task.priority_value >= min_value
        ]

    def explain_plan(self) -> list:
        """Format each scheduled entry into a human-readable string."""
        if not self.schedule:
            return ["No schedule built yet. Call build_schedule() first."]
        explanations = []
        for entry in self.schedule:
            line = (
                f"{entry['start_time']} — {entry['task']} for {entry['pet']} "
                f"({entry['duration']} min, {entry['priority']} priority, due {entry['due_time']})"
            )
            explanations.append(line)
        return explanations
