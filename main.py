from pawpal_system import Owner, Pet, Task, Scheduler

# Create owner
owner = Owner(name="Jordan")

# Create pets
mochi = Pet(name="Mochi", species="dog")
luna = Pet(name="Luna", species="cat")

# Add tasks to Mochi
mochi.add_task(Task(title="Morning walk", due_time="9:30 AM", duration_minutes=30, priority="high"))
mochi.add_task(Task(title="Feeding", due_time="10:00 AM", duration_minutes=10, priority="high"))
mochi.add_task(Task(title="Grooming", due_time="2:00 PM", duration_minutes=20, priority="medium"))

# Add tasks to Luna
luna.add_task(Task(title="Litter box cleaning", due_time="11:00 AM", duration_minutes=10, priority="high"))
luna.add_task(Task(title="Playtime", due_time="3:00 PM", duration_minutes=15, priority="low"))

# Add pets to owner
owner.add_pet(mochi)
owner.add_pet(luna)

# Build schedule
scheduler = Scheduler(owner=owner)
scheduler.build_schedule()

# Print today's schedule
print(f"Today's Schedule for {owner.name}\n")
print("-" * 50)
for line in scheduler.explain_plan():
    print(line)
