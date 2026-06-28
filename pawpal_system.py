from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    title: str
    due_time: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    completed: bool = False
    recurs: str = None        # "daily", "weekly", or None
    due_date: date = None     # the calendar date this task is due
    priority_value: int = field(init=False)

    def __post_init__(self):
        """Map priority string to a numeric value for sorting."""
        mapping = {"low": 1, "medium": 2, "high": 3}
        self.priority_value = mapping.get(self.priority, 0)

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self):
        """Return a new Task for the next occurrence if this task recurs, else None."""
        if self.recurs is None or self.due_date is None:
            return None
        if self.recurs == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.recurs == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            title=self.title,
            due_time=self.due_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurs=self.recurs,
            due_date=next_date,
        )


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

    def complete_task(self, task: Task):
        """Mark a task complete and auto-append its next occurrence if it recurs."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task:
            self.tasks.append(next_task)
        return next_task


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

    def build_schedule(self, sort_by: str = "due_time"):
        """Sort tasks by the chosen strategy and fit them into the available time budget."""
        self.schedule = []
        all_tasks = self.get_all_tasks()
        sorted_tasks = self.sort_tasks(all_tasks, sort_by=sort_by)

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

    def _time_to_minutes(self, time_str: str) -> int:
        """Convert a time string like '9:30 AM' to total minutes since midnight."""
        hour, minute = self._parse_time(time_str)
        return hour * 60 + minute

    def sort_tasks(self, tasks: list, sort_by: str = "due_time") -> list:
        """Sort (pet, task) tuples by 'due_time', 'priority', or 'due_time_priority' (deadline first, priority as tiebreaker)."""
        if sort_by == "due_time":
            return sorted(tasks, key=lambda pt: self._time_to_minutes(pt[1].due_time))
        elif sort_by == "priority":
            return sorted(tasks, key=lambda pt: pt[1].priority_value, reverse=True)
        elif sort_by == "due_time_priority":
            return sorted(tasks, key=lambda pt: (self._time_to_minutes(pt[1].due_time), -pt[1].priority_value))
        else:
            return tasks

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

    def filter_tasks(self, pet_name: str = None, status: str = None) -> list:
        """Return (pet, task) tuples optionally narrowed by pet name and/or status ('pending' or 'completed')."""
        results = self.get_all_tasks()
        if pet_name is not None:
            results = [pt for pt in results if pt[0].name.lower() == pet_name.lower()]
        if status == "pending":
            results = [pt for pt in results if not pt[1].completed]
        elif status == "completed":
            results = [pt for pt in results if pt[1].completed]
        return results

    def detect_conflicts(self) -> list[str]:
        """Check the built schedule for overlapping time windows and return warning strings — never raises."""
        if not self.schedule:
            return ["Warning: No schedule built yet. Call build_schedule() first."]

        warnings = []

        # Pre-compute time windows, skipping any entry that can't be parsed
        windows = []
        for entry in self.schedule:
            try:
                start = self._time_to_minutes(entry["start_time"])
                end = start + entry["duration"]
                windows.append((start, end, entry))
            except (ValueError, KeyError):
                warnings.append(f"Warning: Could not parse time for '{entry.get('task', 'unknown')}' — skipped.")

        # Check every unique pair for overlap
        for i in range(len(windows)):
            for j in range(i + 1, len(windows)):
                start_a, end_a, entry_a = windows[i]
                start_b, end_b, entry_b = windows[j]
                if start_a < end_b and start_b < end_a:
                    end_a_str = self._format_time(end_a // 60, end_a % 60)
                    end_b_str = self._format_time(end_b // 60, end_b % 60)
                    warnings.append(
                        f"Warning: '{entry_a['task']}' ({entry_a['pet']}, "
                        f"{entry_a['start_time']}–{end_a_str}) overlaps with "
                        f"'{entry_b['task']}' ({entry_b['pet']}, "
                        f"{entry_b['start_time']}–{end_b_str})"
                    )

        return warnings if warnings else ["No conflicts detected."]

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
