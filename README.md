# PawPal+ — Pet Care Scheduling System

A professional-grade **Streamlit web application** that intelligently schedules pet care tasks based on owner availability, task priorities, and time constraints. Built with a clean separation of concerns: backend business logic, interactive Streamlit UI, and comprehensive test suite.

---

## ✨ Features

### Core Functionality
- **Pet & Owner Management**: Create multiple pet profiles with associated care tasks
- **Task Scheduling**: Intelligent daily schedule generation prioritizing high-priority tasks
- **Constraint Satisfaction**: Respects owner availability windows and task duration estimates
- **Conflict Detection**: Automatic detection and warning for task time overlaps

### Advanced Algorithms
- **Smart Sorting**: Tasks sortable by priority level or duration (ascending/descending)
- **Flexible Filtering**: Filter tasks by priority, completion status, or search keywords
- **Recurring Tasks**: Automatic generation of recurring task instances with completion tracking
- **Feasibility Analysis**: Validates whether all high-priority tasks fit within owner availability
- **Task Aggregation**: Cross-pet queries for high-priority tasks, incomplete tasks by pet, etc.

### User Experience
- **Interactive Web UI**: Streamlit-based responsive interface with real-time feedback
- **Session State Persistence**: Owner and pet data persists across page refreshes
- **Multi-view Display**: Toggle between all tasks, priority-filtered, status-filtered, or search results
- **Schedule Analytics**: Displays schedule utilization, available time, and conflict warnings
- **Intuitive Task Management**: Single-click task completion with automatic recurring instance creation

---

## 🏗️ Architecture

### Three-Layer Design Pattern

**1. Business Logic Layer** (`pawpal_system.py`)
- `Task` — Pet care activities with priority, frequency, and completion tracking
- `Pet` — Pet profiles managing task collections with filtering methods
- `Owner` — Pet owner profile managing multiple pets and availability constraints
- `Scheduler` — Schedule generation with sorting, filtering, and conflict detection
- `ScheduledTask` — Wraps tasks with specific time slots and overlap detection

**2. User Interface Layer** (`app.py`)
- Streamlit-based responsive web interface
- Session state management for Owner persistence
- Sidebar: Owner profile and pet management
- Main area: Task display with filtering/sorting, schedule generation and analytics
- Direct integration with Scheduler methods for algorithm visibility

**3. Testing Layer** (`tests/test_pawpal.py`)
- 41 comprehensive unit tests covering all classes and algorithms
- 100% pass rate with <200ms execution time
- Test organization: Task, Pet, Owner, Scheduler, and 4+ algorithm test classes

### Class Relationships
```
Owner (1) ─→ (*) Pet ─→ (*) Task
Scheduler ─→ Owner
Scheduler ─→ (*) ScheduledTask
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd Module2-Show-PawPal

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the Streamlit app
streamlit run app.py

# Or run the command-line demo
python main.py
```

The app will open at `http://localhost:8501` in your default browser.

---

## 📁 Project Structure

```
Module2-Show-PawPal/
├── app.py              # Streamlit web interface
├── pawpal_system.py    # Core business logic (5 classes, 25+ methods)
├── main.py             # Command-line demo scenarios
├── tests/
│   └── test_pawpal.py  # 41 unit tests
├── requirements.txt    # Project dependencies
├── README.md           # This file
└── reflection.md       # Design decisions & AI collaboration notes
```

---

## 🧬 API Reference

### Task Class
```python
task = Task(name="Walk", description="30-min walk", priority="high", 
            frequency="daily", duration_minutes=30)
task.mark_complete() → Optional[Task]  # Returns new recurring instance if applicable
task.is_overdue() → bool
```

### Pet Class
```python
pet = Pet(name="Buddy", species="Dog")
pet.add_task(task)
pet.get_tasks_by_priority("high") → List[Task]
pet.get_tasks_by_status(completed=False) → List[Task]
pet.search_tasks("walk") → List[Task]
```

### Owner Class
```python
owner = Owner(name="Alice", availability_start_hour=9, availability_end_hour=17)
owner.add_pet(pet)
owner.get_pet_by_name("Buddy") → Optional[Pet]
owner.get_all_high_priority_tasks() → List[Task]
owner.get_incomplete_tasks_by_pet("Buddy") → List[Task]
```

### Scheduler Class
```python
scheduler = Scheduler(owner)
schedule = scheduler.generate_schedule() → List[ScheduledTask]
scheduler.sort_tasks_by_priority(tasks) → List[Task]
scheduler.filter_tasks_by_priority(tasks, "high") → List[Task]
scheduler.detect_conflicts() → List[tuple]
scheduler.is_schedule_feasible() → bool
```

---

## 🧪 Testing PawPal+

Run the comprehensive test suite:

```bash
pytest tests/test_pawpal.py -v
```

**Test Coverage**: 41 tests across 6 test classes
- **Task Tests** (4): Initialization, equality, completion, and string representation
- **Pet Tests** (5): Task management, filtering, searching, and status tracking
- **Owner Tests** (4): Pet management, task aggregation, and availability tracking
- **Scheduler Tests** (3): Schedule generation, feasibility checks, and conflict detection
- **Sorting Algorithm Tests** (3): Priority-based and duration-based sorting
- **Filtering Algorithm Tests** (6): Priority, status, and empty list filtering
- **Recurring Tasks Tests** (5): Mark completion, optional instance generation, frequency handling
- **Conflict Detection Tests** (6): Overlap detection, conflict summaries, and edge cases
- **Advanced Querying Tests** (5): Cross-pet queries, aggregation, and edge cases

**Confidence Level**: ⭐⭐⭐⭐⭐ (5/5 stars)
- All 41 tests passing
- Execution time: <200ms
- Edge cases covered: empty lists, non-existent data, boundary conditions
- Integration tests validate inter-class workflows

---

## 🎨 Key Design Decisions

### 1. Task.mark_complete() Returns Optional[Task]
Rather than silently auto-generating recurring instances, `mark_complete()` returns the new instance (or None) explicitly. This gives the UI and caller full control over persistence and task list updates.

### 2. Greedy Scheduler with Priority Sorting
The scheduler uses a greedy algorithm: sort tasks by priority (high→medium→low), then schedule in order, fitting as many high-priority tasks as possible within owner availability. This guarantees high-priority tasks never get bumped for lower-priority ones.

### 3. O(n²) Conflict Detection
While interval trees offer O(n log n) conflict detection, we chose simple pairwise overlap checking because typical schedules have 10–15 tasks (no performance bottleneck) and the straightforward approach is more readable and maintainable.

### 4. Clean Separation of Concerns
- Business logic (`pawpal_system.py`) has zero Streamlit dependencies
- UI (`app.py`) imports and uses Scheduler methods directly
- Tests validate behavior without UI dependencies
- This enables easy swapping of UI frameworks or adding CLI tools (`main.py`)

---

## 📈 Smarter Scheduling Features

| Feature | Algorithm | Complexity |
|---------|-----------|-----------|
| Task Sorting | Lambda-based `sorted()` with custom key | O(n log n) |
| Priority Filtering | List comprehension | O(n) |
| Status Filtering | List comprehension | O(n) |
| Keyword Search | Case-insensitive substring matching | O(n) |
| Recurring Generation | Factory pattern in `mark_complete()` | O(1) |
| Conflict Detection | Pairwise overlap checking | O(n²) |
| Schedule Generation | Greedy priority-based ordering | O(n) |
| Task Aggregation | Nested loop traversal | O(n × m) |

---

## 💡 Development Workflow

This project was built in 6 iterative phases:

1. **Phase 1**: System design with UML class diagrams and class stubs
2. **Phase 2**: Core implementation of all 5 classes with 16 unit tests
3. **Phase 3**: Streamlit UI integration with session state persistence
4. **Phase 4**: Algorithmic enhancements (sorting, filtering, conflict detection) and 25 new tests
5. **Phase 5**: Comprehensive testing documentation and validation (41 tests, 100% pass rate)
6. **Phase 6**: UI polish with algorithm visibility, final UML, comprehensive documentation

---

## 📝 License

This project was developed as coursework for AI110 (Winter 2026), Module 2.

For more details on design decisions, AI collaboration strategies, and reflections, see [reflection.md](reflection.md).
