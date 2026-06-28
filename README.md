# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Jordan

--------------------------------------------------
9:00 AM — Morning walk for Mochi (30 min, high priority, due 9:30 AM)
9:30 AM — Feeding for Mochi (10 min, high priority, due 10:00 AM)
9:40 AM — Litter box cleaning for Luna (10 min, high priority, due 11:00 AM)
9:50 AM — Grooming for Mochi (20 min, medium priority, due 2:00 PM)
10:10 AM — Playtime for Luna (15 min, low priority, due 3:00 PM)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest tests/test_pawpal.py -v
```

The test suite covers 17 behaviors across two categories:

**Happy paths** — verifies that core features work correctly under normal use:
- Sorting tasks by due time and priority produces the correct order
- Filtering by pet name and completion status returns the right tasks
- Daily and weekly recurring tasks advance their due date by the correct interval
- Completing a recurring task automatically appends the next occurrence
- Conflict detection returns clean when all tasks finish on time, and warns when a task is pushed past its deadline

**Edge cases** — verifies the system handles boundary conditions without crashing:
- Completing a non-recurring task does not append a new task
- `next_occurrence()` returns `None` when no due date is set
- Filtering with no matching pet returns an empty list
- `detect_conflicts()` returns a warning before a schedule is built
- A task too long for the time budget lands in `skipped`, not `schedule`
- All-completed tasks produce an empty schedule

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0 -- /Library/Frameworks/Python.framework/Versions/3.13/bin/python3
cachedir: .pytest_cache
rootdir: /Users/dylancocoletzi/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collecting ... collected 17 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  5%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 11%]
tests/test_pawpal.py::test_sort_by_due_time_orders_earliest_first PASSED [ 17%]
tests/test_pawpal.py::test_sort_by_priority_orders_high_first PASSED     [ 23%]
tests/test_pawpal.py::test_filter_by_pet_name_returns_only_that_pet PASSED [ 29%]
tests/test_pawpal.py::test_filter_by_pending_excludes_completed PASSED   [ 35%]
tests/test_pawpal.py::test_daily_recurring_task_advances_by_one_day PASSED [ 41%]
tests/test_pawpal.py::test_weekly_recurring_task_advances_by_seven_days PASSED [ 47%]
tests/test_pawpal.py::test_complete_recurring_task_appends_next_occurrence PASSED [ 52%]
tests/test_pawpal.py::test_no_conflict_when_tasks_finish_on_time PASSED  [ 58%]
tests/test_pawpal.py::test_conflict_fires_when_task_finishes_after_deadline PASSED [ 64%]
tests/test_pawpal.py::test_complete_non_recurring_task_does_not_append PASSED [ 70%]
tests/test_pawpal.py::test_next_occurrence_returns_none_without_due_date PASSED [ 76%]
tests/test_pawpal.py::test_filter_returns_empty_list_when_no_match PASSED [ 82%]
tests/test_pawpal.py::test_detect_conflicts_warns_before_schedule_is_built PASSED [ 88%]
tests/test_pawpal.py::test_task_too_long_goes_to_skipped PASSED          [ 94%]
tests/test_pawpal.py::test_all_completed_tasks_produce_empty_schedule PASSED [100%]

============================== 17 passed in 0.02s ==============================
```

**Confidence Level: ★★★★☆ (4/5)**

The scheduling logic, filtering, recurring tasks, and conflict detection all pass their tests with no failures. The main gap is UI behavior — the Streamlit app itself is not covered by automated tests, so interactions like marking a task complete or generating a schedule from the UI are verified manually rather than automatically. A full 5/5 would require end-to-end UI testing.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_tasks()`, `Scheduler._time_to_minutes()` | Supports three strategies: `due_time` (earliest deadline first), `priority` (high → low), and `due_time_priority` (deadline first, priority as tiebreaker). Time strings like "9:30 AM" are converted to total minutes for reliable numeric comparison. |
| Filtering | `Scheduler.filter_tasks()` | Filters pending (pet, task) tuples by pet name, completion status (`"pending"` / `"completed"`), or both combined. Case-insensitive pet name matching. |
| Conflict handling | `Scheduler.detect_conflicts()` | After `build_schedule()` runs, checks every unique pair of scheduled entries for overlapping time windows using the interval overlap formula: `start_A < end_B AND start_B < end_A`. Returns warning strings and never raises an exception. |
| Recurring tasks | `Task.next_occurrence()`, `Pet.complete_task()` | Tasks marked `recurs="daily"` or `recurs="weekly"` automatically generate a new instance with a `due_date` advanced by `timedelta(days=1)` or `timedelta(weeks=1)` when completed via `Pet.complete_task()`. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
