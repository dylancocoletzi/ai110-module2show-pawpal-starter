from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Jordan")

# Create pets
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

today = date.today()

# Add tasks OUT OF ORDER to test sorting
# Feeding and Litter box are daily recurring tasks
mochi.add_task(Task(title="Grooming", due_time="2:00 PM", duration_minutes=20, priority="medium"))
mochi.add_task(Task(title="Morning walk", due_time="9:30 AM", duration_minutes=30, priority="high"))
mochi.add_task(Task(title="Feeding", due_time="10:00 AM", duration_minutes=10, priority="high", recurs="daily", due_date=today))

luna.add_task(Task(title="Playtime", due_time="3:00 PM", duration_minutes=15, priority="low"))
luna.add_task(Task(title="Litter box cleaning", due_time="11:00 AM", duration_minutes=10, priority="high", recurs="daily", due_date=today))

# Mark one task completed to test status filter
mochi.tasks[1].mark_complete()  # Morning walk is done (not recurring)

# Add pets to owner
owner.add_pet(mochi)
owner.add_pet(luna)

scheduler = Scheduler(owner=owner)

# --- Sort by due_time ---
print("=== Sorted by Due Time ===")
scheduler.build_schedule(sort_by="due_time")
for line in scheduler.explain_plan():
    print(line)

print()

# --- Sort by priority ---
print("=== Sorted by Priority ===")
scheduler.build_schedule(sort_by="priority")
for line in scheduler.explain_plan():
    print(line)

print()

# --- Sort by due_time + priority tiebreaker ---
print("=== Sorted by Due Time + Priority ===")
scheduler.build_schedule(sort_by="due_time_priority")
for line in scheduler.explain_plan():
    print(line)

print()

# --- Filter: all pending tasks ---
print("=== Filter: All Pending Tasks ===")
for pet, task in scheduler.filter_tasks(status="pending"):
    print(f"  {pet.name}: {task.title} (due {task.due_time})")

print()

# --- Filter: Mochi's tasks only ---
print("=== Filter: Mochi's Tasks ===")
for pet, task in scheduler.filter_tasks(pet_name="Mochi"):
    status = "done" if task.completed else "pending"
    print(f"  {task.title} — {status} (due {task.due_time})")

print()

# --- Filter: Luna's pending tasks ---
print("=== Filter: Luna's Pending Tasks ===")
for pet, task in scheduler.filter_tasks(pet_name="Luna", status="pending"):
    print(f"  {task.title} (due {task.due_time}, {task.priority} priority)")

print()

# --- Conflict detection: flags tasks that finish after their due_time ---
print("=== Conflict Detection (deadline misses) ===")
# Sort by priority so high-priority tasks go first regardless of due time.
# This can push a short-deadline task late enough to miss its deadline.
scheduler.build_schedule(sort_by="priority")
for line in scheduler.detect_conflicts():
    print(line)

print()

# --- Recurring tasks demo ---
print("=== Recurring Tasks Demo ===")
feeding = mochi.tasks[2]   # Feeding — daily recurring
litter  = luna.tasks[1]    # Litter box — daily recurring

print(f"Completing '{feeding.title}' for Mochi (due {feeding.due_date}, recurs={feeding.recurs})")
next_feeding = mochi.complete_task(feeding)
print(f"  → Next occurrence created: due {next_feeding.due_date}")

print(f"Completing '{litter.title}' for Luna (due {litter.due_date}, recurs={litter.recurs})")
next_litter = luna.complete_task(litter)
print(f"  → Next occurrence created: due {next_litter.due_date}")

print()
print("Mochi's tasks after completion:")
for t in mochi.tasks:
    status = "done" if t.completed else "pending"
    recur_label = f", recurs={t.recurs}" if t.recurs else ""
    print(f"  [{status}] {t.title} (due_date={t.due_date}{recur_label})")
