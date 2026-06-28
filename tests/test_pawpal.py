from datetime import date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler


# --- Helpers ---

def make_scheduler(*pets):
    owner = Owner(name="Jordan")
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner=owner)


# --- Existing tests ---

def test_mark_complete_changes_status():
    task = Task(title="Morning walk", due_time="9:30 AM", duration_minutes=30, priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.list_tasks()) == 0
    pet.add_task(Task(title="Feeding", due_time="10:00 AM", duration_minutes=10, priority="high"))
    assert len(pet.list_tasks()) == 1


# --- Happy Path: Sorting ---

def test_sort_by_due_time_orders_earliest_first():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Grooming", due_time="2:00 PM", duration_minutes=20, priority="medium"))
    pet.add_task(Task(title="Walk", due_time="9:30 AM", duration_minutes=30, priority="high"))
    scheduler = make_scheduler(pet)
    scheduler.build_schedule(sort_by="due_time")
    assert scheduler.schedule[0]["task"] == "Walk"
    assert scheduler.schedule[1]["task"] == "Grooming"


def test_sort_by_priority_orders_high_first():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Playtime", due_time="3:00 PM", duration_minutes=15, priority="low"))
    pet.add_task(Task(title="Feeding", due_time="10:00 AM", duration_minutes=10, priority="high"))
    scheduler = make_scheduler(pet)
    scheduler.build_schedule(sort_by="priority")
    assert scheduler.schedule[0]["task"] == "Feeding"
    assert scheduler.schedule[1]["task"] == "Playtime"


# --- Happy Path: Filtering ---

def test_filter_by_pet_name_returns_only_that_pet():
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    mochi.add_task(Task(title="Walk", due_time="9:30 AM", duration_minutes=30, priority="high"))
    luna.add_task(Task(title="Playtime", due_time="3:00 PM", duration_minutes=15, priority="low"))
    scheduler = make_scheduler(mochi, luna)
    results = scheduler.filter_tasks(pet_name="Mochi")
    assert len(results) == 1
    assert all(pet.name == "Mochi" for pet, task in results)


def test_filter_by_pending_excludes_completed():
    pet = Pet(name="Mochi", species="dog")
    t1 = Task(title="Walk", due_time="9:30 AM", duration_minutes=30, priority="high")
    t2 = Task(title="Feeding", due_time="10:00 AM", duration_minutes=10, priority="high")
    t1.mark_complete()
    pet.add_task(t1)
    pet.add_task(t2)
    scheduler = make_scheduler(pet)
    results = scheduler.filter_tasks(status="pending")
    assert len(results) == 1
    assert results[0][1].title == "Feeding"


# --- Happy Path: Recurring Tasks ---

def test_daily_recurring_task_advances_by_one_day():
    today = date.today()
    task = Task(title="Feeding", due_time="10:00 AM", duration_minutes=10,
                priority="high", recurs="daily", due_date=today)
    next_task = task.next_occurrence()
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)


def test_weekly_recurring_task_advances_by_seven_days():
    today = date.today()
    task = Task(title="Bath", due_time="11:00 AM", duration_minutes=20,
                priority="medium", recurs="weekly", due_date=today)
    next_task = task.next_occurrence()
    assert next_task.due_date == today + timedelta(weeks=1)


def test_complete_recurring_task_appends_next_occurrence():
    today = date.today()
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Feeding", due_time="10:00 AM", duration_minutes=10,
                priority="high", recurs="daily", due_date=today)
    pet.add_task(task)
    pet.complete_task(task)
    assert len(pet.list_tasks()) == 2
    assert pet.list_tasks()[1].due_date == today + timedelta(days=1)


# --- Happy Path: Conflict Detection ---

def test_no_conflict_when_tasks_finish_on_time():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", due_time="9:30 AM", duration_minutes=30, priority="high"))
    scheduler = make_scheduler(pet)
    scheduler.build_schedule(sort_by="due_time")
    assert scheduler.detect_conflicts() == ["No conflicts detected."]


def test_conflict_fires_when_task_finishes_after_deadline():
    pet = Pet(name="Mochi", species="dog")
    # Grooming due 9:30 AM but low priority — gets pushed behind Feeding
    pet.add_task(Task(title="Grooming", due_time="9:30 AM", duration_minutes=30, priority="low"))
    pet.add_task(Task(title="Feeding", due_time="10:00 AM", duration_minutes=10, priority="high"))
    scheduler = make_scheduler(pet)
    scheduler.build_schedule(sort_by="priority")
    conflicts = scheduler.detect_conflicts()
    assert any("Grooming" in w for w in conflicts)


# --- Edge Cases ---

def test_complete_non_recurring_task_does_not_append():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Vet visit", due_time="2:00 PM", duration_minutes=60, priority="high")
    pet.add_task(task)
    pet.complete_task(task)
    assert len(pet.list_tasks()) == 1


def test_next_occurrence_returns_none_without_due_date():
    task = Task(title="Feeding", due_time="10:00 AM", duration_minutes=10,
                priority="high", recurs="daily")
    assert task.next_occurrence() is None


def test_filter_returns_empty_list_when_no_match():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", due_time="9:30 AM", duration_minutes=30, priority="high"))
    scheduler = make_scheduler(pet)
    results = scheduler.filter_tasks(pet_name="Luna")
    assert results == []


def test_detect_conflicts_warns_before_schedule_is_built():
    pet = Pet(name="Mochi", species="dog")
    scheduler = make_scheduler(pet)
    result = scheduler.detect_conflicts()
    assert result == ["Warning: No schedule built yet. Call build_schedule() first."]


def test_task_too_long_goes_to_skipped():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Long session", due_time="5:00 PM", duration_minutes=500, priority="high"))
    scheduler = make_scheduler(pet)
    scheduler.build_schedule()
    assert len(scheduler.schedule) == 0
    assert len(scheduler.skipped) == 1
    assert scheduler.skipped[0]["task"] == "Long session"


def test_all_completed_tasks_produce_empty_schedule():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Walk", due_time="9:30 AM", duration_minutes=30, priority="high")
    task.mark_complete()
    pet.add_task(task)
    scheduler = make_scheduler(pet)
    scheduler.build_schedule()
    assert scheduler.schedule == []
