# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` stored the owner's name and held a single reference to one `Pet`. `Pet` stored only identifying info (name and species). `Task` represented a care task with a title, duration in minutes, and priority level with an auto-computed priority value. `Scheduler` took an owner and a flat list of tasks as input and was responsible for building an ordered daily plan and explaining why each task was selected.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design changed significantly after reviewing the full requirements. First, `Owner` was updated from holding a single `Pet` to a list of pets with `add_pet()` and `list_pets()` methods, because the rubric requires the scheduler to operate across multiple pets. Second, `Pet` gained a tasks collection with `add_task()`, `list_tasks()`, and `pending_tasks()` methods — tasks moved from being passed directly to the `Scheduler` to living on the `Pet` they belong to. Third, `Task` gained a `due_time` field, a `completed` boolean, and a `mark_complete()` method to satisfy the rubric requirement for completion status tracking. Finally, `Scheduler` was updated to aggregate tasks across all pets via `get_all_tasks()` and gained a second algorithmic feature `filter_by_priority()` to meet the requirement of at least two algorithmic features.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
