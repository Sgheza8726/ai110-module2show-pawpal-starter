"""
PawPal+ Demo Script with Algorithmic Features

This enhanced script demonstrates:
1. Sorting and filtering tasks by various criteria
2. Recurring task automation
3. Conflict detection
4. Advanced querying and scheduling features
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import time


def demo_sorting_and_filtering():
    """Demonstrate sorting, filtering, and search functionality."""
    print("\n" + "="*70)
    print("DEMO 1: Sorting and Filtering Tasks")
    print("="*70 + "\n")
    
    # Setup
    owner = Owner(name="Alex", availability_start=time(7, 0), availability_end=time(21, 0))
    dog = Pet(name="Buddy", species="Labrador", age=4)
    owner.add_pet(dog)
    
    # Add tasks with varying priorities and durations (deliberately out of order)
    tasks_to_add = [
        Task("Quick snack", "Treat time", 5, "low", "daily"),
        Task("Evening walk", "Long walk", 45, "high", "daily"),
        Task("Playtime", "Interactive play", 20, "medium", "daily"),
        Task("Medication", "Daily pill", 5, "high", "daily"),
        Task("Grooming", "Brush coat", 15, "low", "weekly"),
        Task("Training", "Practice commands", 30, "medium", "daily"),
    ]
    
    for task in tasks_to_add:
        dog.add_task(task)
    
    print(f"Pet: {dog.name} ({dog.species})")
    print(f"Total tasks added: {len(dog.tasks)}\n")
    
    # Show unsorted tasks
    print("Original task order:")
    for i, task in enumerate(dog.get_daily_tasks(), 1):
        print(f"  {i}. {task.name:20} | {task.duration_minutes:3}min | {task.priority:6} priority")
    
    # Sort by priority
    scheduler = Scheduler(owner)
    sorted_by_priority = scheduler.sort_tasks_by_priority(dog.get_daily_tasks())
    print("\nSorted by priority (HIGH → MEDIUM → LOW):")
    for i, task in enumerate(sorted_by_priority, 1):
        print(f"  {i}. {task.name:20} | {task.duration_minutes:3}min | {task.priority:6} priority")
    
    # Sort by duration (short first)
    sorted_by_duration = scheduler.sort_tasks_by_duration(dog.get_daily_tasks(), ascending=True)
    print("\nSorted by duration (shortest first):")
    for i, task in enumerate(sorted_by_duration, 1):
        print(f"  {i}. {task.name:20} | {task.duration_minutes:3}min | {task.priority:6} priority")
    
    # Filter by priority
    high_priority = scheduler.filter_tasks_by_priority(dog.get_daily_tasks(), "high")
    print(f"\nHigh-priority tasks only ({len(high_priority)} found):")
    for task in high_priority:
        print(f"  • {task.name} ({task.duration_minutes} min)")
    
    # Search functionality
    print("\nSearching for tasks containing 'walk':")
    walk_tasks = dog.search_tasks("walk")
    for task in walk_tasks:
        print(f"  • {task.name}: {task.description}")


def demo_recurring_tasks():
    """Demonstrate automatic recurring task generation."""
    print("\n" + "="*70)
    print("DEMO 2: Recurring Task Automation")
    print("="*70 + "\n")
    
    owner = Owner(name="Jordan")
    cat = Pet(name="Whiskers", species="Cat", age=6)
    owner.add_pet(cat)
    
    # Create a recurring daily task
    feeding_task = Task(
        name="Feed Whiskers",
        description="Morning wet food",
        duration_minutes=10,
        priority="high",
        frequency="daily"
    )
    cat.add_task(feeding_task)
    
    print(f"Original task: {feeding_task.name}")
    print(f"  Status: {'Completed' if feeding_task.is_completed else 'Incomplete'}")
    print(f"  Frequency: {feeding_task.frequency}")
    
    # Mark the task complete - this should generate a new recurring instance
    print("\nMarking task as complete...")
    next_task = feeding_task.mark_complete()
    
    print(f"\nAfter completion:")
    print(f"  Original task status: {'Completed' if feeding_task.is_completed else 'Incomplete'}")
    print(f"  Next occurrence created: {next_task is not None}")
    
    if next_task:
        print(f"\nNew recurring task instance:")
        print(f"  Name: {next_task.name}")
        print(f"  Status: {'Completed' if next_task.is_completed else 'Incomplete'}")
        print(f"  Frequency: {next_task.frequency}")
        print(f"  Priority: {next_task.priority}")
        
        # Add the next instance to the pet
        cat.add_task(next_task)
        print(f"\nTask added to {cat.name}. Total tasks: {len(cat.tasks)}")


def demo_conflict_detection():
    """Demonstrate task conflict detection."""
    print("\n" + "="*70)
    print("DEMO 3: Conflict Detection")
    print("="*70 + "\n")
    
    owner = Owner(name="Sam", availability_start=time(8, 0), availability_end=time(18, 0))
    dog = Pet(name="Max", species="Dog", age=2)
    owner.add_pet(dog)
    
    # Create tasks that will naturally avoid conflicts
    dog.add_task(Task("Morning walk", "Park time", 30, "high", "daily"))
    dog.add_task(Task("Feeding", "Dry kibble", 10, "high", "daily"))
    dog.add_task(Task("Playtime", "Indoor games", 20, "medium", "daily"))
    dog.add_task(Task("Training", "Commands", 25, "medium", "daily"))
    
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule()
    
    print(f"Generated schedule for {owner.name}:")
    print(f"Availability: {owner.availability_start.strftime('%H:%M')} - {owner.availability_end.strftime('%H:%M')}\n")
    
    print(scheduler.get_schedule_summary())
    
    # Check for conflicts
    print("\n" + scheduler.get_conflicts_summary())
    
    # Now simulate a conflict scenario by manually creating overlapping tasks
    print("\n" + "-"*70)
    print("Simulating conflict scenario...")
    print("-"*70)
    
    from pawpal_system import ScheduledTask
    conflict_scheduler = Scheduler(owner)
    
    # Manually create conflicting schedule
    task1 = Task("Task A", "First task", 30, "high", "daily")
    task2 = Task("Task B", "Second task", 30, "high", "daily")
    
    # Schedule both at 9 AM (they will overlap)
    conflict_scheduler.schedule = [
        ScheduledTask(task1, time(9, 0), 30),
        ScheduledTask(task2, time(9, 15), 30),  # Overlaps with first task
    ]
    
    print(f"\nManually created overlapping schedule:")
    print(f"  Task A: 09:00-09:30")
    print(f"  Task B: 09:15-09:45 (overlaps!)\n")
    
    print(conflict_scheduler.get_conflicts_summary())


def demo_advanced_querying():
    """Demonstrate advanced pet and task querying."""
    print("\n" + "="*70)
    print("DEMO 4: Advanced Querying")
    print("="*70 + "\n")
    
    owner = Owner(name="Casey")
    
    # Create multiple pets with different tasks
    dog = Pet(name="Max", species="Dog", age=3)
    cat = Pet(name="Whiskers", species="Cat", age=5)
    rabbit = Pet(name="Hoppy", species="Rabbit", age=2)
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    owner.add_pet(rabbit)
    
    # Add various tasks
    dog.add_task(Task("Morning walk", "Exercise", 30, "high", "daily"))
    dog.add_task(Task("Feeding", "Food", 10, "high", "daily"))
    dog.add_task(Task("Play", "Fun", 20, "medium", "daily"))
    
    cat.add_task(Task("Feeding", "Cat food", 10, "high", "daily"))
    cat.add_task(Task("Litter box", "Cleaning", 5, "high", "daily"))
    cat.add_task(Task("Grooming", "Brushing", 15, "low", "weekly"))
    
    rabbit.add_task(Task("Feeding", "Fresh veggies", 10, "high", "daily"))
    rabbit.add_task(Task("Cage cleaning", "Full clean", 30, "high", "weekly"))
    
    # Query by pet name
    print(f"Owner: {owner.name} manages {len(owner.pets)} pets\n")
    
    found_pet = owner.get_pet_by_name("whiskers")
    if found_pet:
        print(f"Found pet by name search: {found_pet.name} ({found_pet.species})")
        print(f"  Daily tasks: {len(found_pet.get_daily_tasks())}")
    
    # Get all high-priority tasks
    high_priority_tasks = owner.get_all_high_priority_tasks()
    print(f"\nAll high-priority daily tasks: {len(high_priority_tasks)}")
    for task in high_priority_tasks:
        print(f"  • {task.name}")
    
    # Get incomplete tasks organized by pet
    print("\nIncomplete tasks by pet:")
    incomplete_by_pet = owner.get_incomplete_tasks_by_pet()
    for pet_name, tasks in incomplete_by_pet.items():
        print(f"  {pet_name}: {len(tasks)} incomplete")
        for task in tasks:
            print(f"    - {task.name}")


def main():
    """Run all demo scenarios."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "PawPal+ ALGORITHMIC FEATURES DEMO" + " "*20 + "║")
    print("╚" + "="*68 + "╝")
    
    demo_sorting_and_filtering()
    demo_recurring_tasks()
    demo_conflict_detection()
    demo_advanced_querying()
    
    print("\n" + "="*70)
    print("All demos completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
