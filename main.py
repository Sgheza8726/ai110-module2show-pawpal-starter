"""
PawPal+ Demo Script

This script demonstrates the core functionality of the PawPal+ system by:
1. Creating an owner with pets
2. Adding tasks with different priorities
3. Generating and displaying today's schedule
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import time


def main():
    # Step 1: Create an owner
    owner = Owner(
        name="Sarah",
        availability_start=time(7, 0),
        availability_end=time(21, 0),
        preferences={"ideal_walk_time": "morning"}
    )
    
    # Step 2: Create pets
    dog = Pet(
        name="Max",
        species="Golden Retriever",
        age=3,
        special_needs="Needs 2 walks daily"
    )
    
    cat = Pet(
        name="Whiskers",
        species="Tabby Cat",
        age=5,
        special_needs="Prone to hairballs"
    )
    
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Step 3: Add tasks to the dog
    dog_morning_walk = Task(
        name="Morning Walk",
        description="Let Max stretch his legs in the park",
        duration_minutes=30,
        priority="high",
        frequency="daily"
    )
    dog.add_task(dog_morning_walk)
    
    dog_evening_walk = Task(
        name="Evening Walk",
        description="Get fresh air and exercise",
        duration_minutes=30,
        priority="high",
        frequency="daily"
    )
    dog.add_task(dog_evening_walk)
    
    dog_feeding = Task(
        name="Feed Max",
        description="Give Max his dry kibble",
        duration_minutes=10,
        priority="high",
        frequency="daily"
    )
    dog.add_task(dog_feeding)
    
    dog_playtime = Task(
        name="Playing & Training",
        description="Interactive play session",
        duration_minutes=20,
        priority="medium",
        frequency="daily"
    )
    dog.add_task(dog_playtime)
    
    # Step 4: Add tasks to the cat
    cat_feeding = Task(
        name="Feed Whiskers",
        description="Wet food and fresh water",
        duration_minutes=10,
        priority="high",
        frequency="daily"
    )
    cat.add_task(cat_feeding)
    
    cat_playtime = Task(
        name="Cat Playtime",
        description="15 min interactive play",
        duration_minutes=15,
        priority="medium",
        frequency="daily"
    )
    cat.add_task(cat_playtime)
    
    # Step 5: Create scheduler and generate the schedule
    scheduler = Scheduler(owner)
    
    print("\n" + "="*60)
    print("PawPal+ DEMO - Daily Schedule Generator")
    print("="*60 + "\n")
    
    # Print owner and pet information
    print(f"Owner: {owner.name}")
    print(f"Available: {owner.availability_start.strftime('%H:%M')} - {owner.availability_end.strftime('%H:%M')}")
    print(f"Total available time: {owner.get_total_available_minutes()} minutes\n")
    
    print("Pets and Tasks:")
    for pet in owner.pets:
        print(f"  • {pet.name} ({pet.species}), Age: {pet.age}")
        for task in pet.get_daily_tasks():
            print(f"    - {task.name}: {task.duration_minutes} min [Priority: {task.priority}]")
    
    print(f"\nTotal daily task time: {owner.get_total_daily_task_minutes()} minutes\n")
    
    # Generate and display the schedule
    scheduler.generate_schedule()
    print(scheduler.get_schedule_summary())
    
    # Check feasibility
    if scheduler.is_schedule_feasible():
        print("✓ Schedule is feasible - all high-priority tasks fit!")
    else:
        print("✗ WARNING: Not enough time for all high-priority tasks!")
    
    print("\n" + "="*60)
    print("Testing Task Completion")
    print("="*60 + "\n")
    
    # Test marking tasks as complete
    print(f"Before: {dog_morning_walk.name} - Completed: {dog_morning_walk.is_completed}")
    dog_morning_walk.mark_complete()
    print(f"After:  {dog_morning_walk.name} - Completed: {dog_morning_walk.is_completed}\n")


if __name__ == "__main__":
    main()
