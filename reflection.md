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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
