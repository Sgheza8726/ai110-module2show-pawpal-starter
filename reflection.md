# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

The PawPal+ system is built around four main components:

1. **Owner** – Represents the pet owner with attributes like name, availability, and preferences. This class holds the user's context and constraints that influence scheduling decisions.

2. **Pet** – Represents a pet in the owner's care. Each pet has attributes like name, species, age, and special needs. A single owner can have multiple pets, so Pet is a dependent object.

3. **Task** – Represents a single care task (walk, feed, medicate, play, etc.). Each task captures its duration, priority level (high/medium/low), frequency, and any special requirements. Tasks are what get scheduled.

4. **Scheduler** – The system's decision-maker. It takes all the pets, their tasks, and owner constraints as input, then produces an optimized daily schedule by considering time available, task priorities, and task dependencies.

The core relationship is: **Owner has Pets → Pets have Tasks → Scheduler arranges Tasks into a Plan**. The scheduler acts as the "brain" that balances competing priorities and time constraints to create a feasible daily plan.

**b. Design changes**

During implementation, I made a few refinements to the initial skeleton:

1. **Added Task completion tracking** - The original design didn't explicitly include an `is_completed` field on Task. I added this to track which tasks have been done, which is essential for any real scheduling system.

2. **Created ScheduledTask wrapper class** - Instead of just storing Task objects with times, I wrapped them in a ScheduledTask class that handles time calculations (get_end_time, overlap detection). This separation of concerns makes scheduling logic cleaner.

3. **Enhanced Owner's data access** - I added `get_all_daily_tasks()` and `get_total_daily_task_minutes()` methods to Owner so the Scheduler doesn't need to manually iterate through all pets. This makes the Scheduler cleaner and follows the principle of encapsulation.

4. **Priority-based sorting in Scheduler** - The Scheduler now sorts tasks by priority score before fitting them into the schedule. This ensures high-priority tasks always get scheduled first, which is critical for a pet care app where some tasks (feeding, medication) can't be skipped.

5. **Added multiple frequency types** - Extended beyond just "daily" to support "twice-daily" and "three-times-daily" in the `is_due_today()` method, making the system more flexible.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints:

1. **Time availability**: Each Owner has an `availability_start` and `availability_end` time (e.g., 7 AM to 9 PM). The scheduler respects these bounds and will not schedule tasks outside this window.

2. **Task priority levels**: Each task has a priority of 'high', 'medium', or 'low'. High-priority tasks (like feeding or medication) are scheduled first, ensuring they always fit.

3. **Task duration**: Each task requires a specific number of minutes. The scheduler prevents overlapping tasks and ensures sequential scheduling within available time.

I prioritized **task priority** above all else because in pet care, some tasks cannot be skipped (feeding) or postponed (medication). Owner availability is the binding constraint that prevents over-scheduling.

**b. Tradeoffs**

The main tradeoff is **greedy scheduling vs. optimization**. My current implementation uses a greedy algorithm: sort by priority, then fit tasks sequentially from the start of the day. 

**Why this tradeoff is reasonable**: Pet owners care most that high-priority tasks happen. The greedy approach guarantees this. A more complex optimization algorithm (like bin packing) might produce a "better" schedule by spreading tasks more evenly throughout the day, but it would add implementation complexity without much practical benefit. The simple approach is predictable and easy to verify.

An edge case: If there aren't enough hours for all tasks, the scheduler will leave some low-priority tasks unscheduled. In a future version, we could implement "task rejection" with user feedback ("You have too many tasks for today - which would you like to skip?").

**Additional algorithmic tradeoff in Phase 4**: For **conflict detection**, I chose to check all pairs of scheduled tasks O(n²) rather than implementing a more complex interval tree O(n log n). For a typical day with 10-15 tasks, the overhead is negligible, and the simple approach is more readable. For an app managing 100+ tasks, an interval tree would be better.

For **recurring task automation**, I chose to return a new Task instance rather than silently creating it on the owner's behalf. This gives the app more control—it can choose to add the task, show it to the user first, or discard it. This explicit factory pattern is more flexible than automatic creation..

---

## 3. AI Collaboration

**a. How you used AI**

I used AI tools during this project in several ways:

1. **System design brainstorming** - I asked GitHub Copilot to review my class skeleton and suggest missing relationships or logical bottlenecks.

2. **Test generation** - For the test file, I asked Copilot to draft comprehensive test cases covering the most critical behaviors (task completion, task addition, feasibility checking).

3. **Code quality** - I requested suggestions for improving the human-readability of schedule output, leading to the formatted `ScheduledTask.__str__()` method that displays times clearly.

The most helpful prompts were specific and included code examples: "Here's my Task class skeleton - what methods am I missing for a pet care system?" This is much better than vague questions like "Help me design classes."

**b. Judgment and verification**

When Copilot suggested adding a `ScheduledTask` wrapper class, I initially questioned whether it was necessary. My first instinct was to just store tuples of (task, time). However, I test-drove both approaches and realized the wrapper class made time calculations and overlap detection much cleaner with dedicated methods. I verified this by writing tests that would have been more complex without the wrapper.

Another moment: Copilot suggested using a two-step dispatch (Owner → Pet → Task) to retrieve all tasks. I verified this was correct by hand-tracing a scenario with multiple pets and confirming all tasks were collected properly.

---

## 4. Testing and Verification

**a. What you tested**

I created 16 unit tests across 5 test classes:

1. **Task tests** (5 tests): Verified task completion marking, frequency detection (is_due_today), and priority scoring.

2. **Pet tests** (4 tests): Verified adding single and multiple tasks, filtering to daily tasks only, and summing task durations correctly.

3. **Owner tests** (4 tests): Verified adding pets, calculating available minutes, retrieving all daily tasks across all pets, and summing total task minutes.

4. **Scheduler tests** (3 tests): Verified schedule generation actually schedules tasks, feasibility checking detects when high-priority tasks fit, and infeasibility is correctly detected.

These tests were important because they verify the core logic that pet owners depend on: Task tracking, availability calculations, and schedule feasibility. If these fail, the whole system breaks.

**b. Confidence**

I'm quite confident the scheduler works correctly for the happy path (tasks fit within available time). All 16 tests pass with 100% success rate.

Edge cases I would test next if I had more time:

1. **Overlapping task times** - What if the owner specifies they can only work 7-8 AM? Can we handle ultra-short availability windows?

2. **Multiple frequency types** - Test "twice-daily" and "three-times-daily" tasks to ensure they're filtered correctly by `is_due_today()`.

3. **Empty schedules** - What if an owner has no pets or no tasks? Does the system gracefully handle empty lists?

4. **Task duration edge cases** - What if a task is 1,440 minutes (a full day)? What if a task is 0 minutes?

5. **Integration with Streamlit** - End-to-end testing once the UI is connected to verify data flows correctly from form input to schedule display.

---

## 5. Reflection

**a. What went well**

The part of this project I'm most satisfied with is the **separation of concerns** in my architecture. Each class has a clear, single responsibility:

- **Task**: Knows about itself (duration, priority, completion status)
- **Pet**: Manages a collection of tasks and can answer questions about them
- **Owner**: Manages multiple pets and aggregates their data
- **Scheduler**: Makes decisions about task ordering without worrying about data storage

This design made testing straightforward and the demo script easy to understand. Someone reading the code can quickly see what each class does.

Also, all tests passing on the first run was a good sign that the design was sound.

**b. What you would improve**

If I had another iteration, I would:

1. **Add a Plan class** - Right now, Scheduler returns a list of ScheduledTasks. I'd create a Plan class that wraps the schedule, includes metadata (total time, feasibility flag, any tasks that didn't fit), and a more detailed explanation of why tasks were scheduled in this order.

2. **Support task dependencies** - Some tasks should happen before others (e.g., "Feed Max" should come before "Clean food bowl"). The current scheduler doesn't enforce this.

3. **Add scheduling preferences** - Owners might prefer their dog's walk in the morning (for their own routine). I'd enhance Owner.preferences to be more structured and have the Scheduler respect these soft constraints.

4. **Persist data** - Right now, everything exists only in memory. Adding a simple JSON-based persistence layer would let owners save and reload their schedules.

**c. Key takeaway**

The biggest lesson I learned is that **good design upfront saves massive implementation effort later**. Because I spent 45 minutes on the UML diagram and class skeleton, the actual implementation felt straightforward. Each class knew exactly what it should do. There was no "Well, should this logic go in Pet or Owner?" confusion.

Working with AI was most effective when I was specific and provided code context. Vague questions like "Help me with my scheduler" got vague answers. Specific questions like "Here's my skeleton - should the Scheduler directly access pets or ask the Owner for aggregated data?" gave me actionable insights I could evaluate and verify.
