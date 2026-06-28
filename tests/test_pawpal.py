from pawpal_system import Owner, Pet, Task, Scheduler


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
