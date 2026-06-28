# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design included four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. `Owner` stores the owner's name and holds a reference to their `Pet`. `Pet` stores the pet's name and species. `Task` represents a single care task with a title, duration in minutes, and priority level. `Scheduler` takes an owner and a list of tasks and is responsible for building an ordered daily plan based on constraints and explaining why each task was selected.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, the design changed in three ways after reviewing the skeleton against the requirements. First, I added a `preferences` field to `Owner` because the requirements specify "basic info and preferences" but the initial design only stored a name. Second, I added a `start_time` attribute to `Scheduler` because without a day start anchor (e.g. `"9:00 AM"`), `explain_plan()` could not generate meaningful timestamps for each task. Third, I identified that `explain_plan()` needed a guard to handle being called before `build_schedule()` — without it, the method would silently return an empty list with no indication that the schedule had not been built yet.

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
