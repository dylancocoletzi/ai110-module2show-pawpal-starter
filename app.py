import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None

# --- Owner Section ---
st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

if st.button("Set Owner"):
    st.session_state.owner = Owner(name=owner_name)
    st.success(f"Owner set to {owner_name}")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
    st.stop()

owner = st.session_state.owner

# --- Pets Section ---
st.divider()
st.subheader("Pets")

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name} ({species})")

if owner.list_pets():
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species} for p in owner.list_pets()])
else:
    st.info("No pets yet. Add one above.")

# --- Tasks Section ---
if owner.list_pets():
    st.divider()
    st.subheader("Tasks")

    pet_names = [p.name for p in owner.list_pets()]
    selected_pet_name = st.selectbox("Add task to", pet_names)
    selected_pet = next(p for p in owner.list_pets() if p.name == selected_pet_name)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        due_time = st.text_input("Due time", value="10:00 AM")
    with col3:
        duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    col5, col6 = st.columns(2)
    with col5:
        recurs_input = st.selectbox("Repeats", ["none", "daily", "weekly"])
    with col6:
        due_date_input = st.date_input("Due date", value=date.today())

    if st.button("Add Task"):
        recurs = recurs_input if recurs_input != "none" else None
        selected_pet.add_task(Task(
            title=task_title,
            due_time=due_time,
            duration_minutes=int(duration),
            priority=priority,
            recurs=recurs,
            due_date=due_date_input,
        ))
        st.success(f"Added '{task_title}' to {selected_pet_name}")

    for pet in owner.list_pets():
        if pet.list_tasks():
            st.markdown(f"**{pet.name}'s tasks:**")
            st.table([{
                "title": t.title,
                "due_time": t.due_time,
                "duration (min)": t.duration_minutes,
                "priority": t.priority,
                "completed": t.completed
            } for t in pet.list_tasks()])

# --- Filter Section ---
if owner.list_pets():
    st.divider()
    st.subheader("Filter Tasks")

    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        filter_pet = st.selectbox("Filter by pet", ["All pets"] + [p.name for p in owner.list_pets()])
    with filter_col2:
        filter_status = st.selectbox("Filter by status", ["all", "pending", "completed"])

    if st.button("Apply Filter"):
        scheduler = Scheduler(owner=owner)
        pet_name_arg = None if filter_pet == "All pets" else filter_pet
        status_arg = None if filter_status == "all" else filter_status
        results = scheduler.filter_tasks(pet_name=pet_name_arg, status=status_arg)
        if results:
            st.table([{
                "pet": pet.name,
                "task": task.title,
                "due_time": task.due_time,
                "priority": task.priority,
                "status": "completed" if task.completed else "pending",
                "recurs": task.recurs or "—",
            } for pet, task in results])
        else:
            st.info("No tasks match the selected filters.")

# --- Schedule Section ---
st.divider()
st.subheader("Build Schedule")

sort_by = st.selectbox(
    "Sort tasks by",
    ["due_time", "priority", "due_time_priority"],
    format_func=lambda x: {
        "due_time": "Due time (earliest first)",
        "priority": "Priority (high → low)",
        "due_time_priority": "Due time + priority tiebreaker",
    }[x]
)

if st.button("Generate schedule"):
    if not owner.list_pets():
        st.warning("Add at least one pet before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner)
        scheduler.build_schedule(sort_by=sort_by)
        plan = scheduler.explain_plan()
        st.success(f"Schedule built for {owner.name}!")
        for line in plan:
            st.write(line)

        conflicts = scheduler.detect_conflicts()
        if conflicts != ["No conflicts detected."]:
            st.divider()
            st.markdown("**Scheduling Conflicts**")
            for warning in conflicts:
                st.warning(warning)
        else:
            st.info("No conflicts detected.")
