"""
Tests for PawPal+ System

This module contains unit tests for the core PawPal+ functionality,
including basic operations, scheduling, and advanced algorithmic features.
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler, ScheduledTask
from datetime import time


class TestTask:
    """Test cases for the Task class."""
    
    def test_mark_complete(self):
        """Verify that marking a task complete actually changes its status."""
        task = Task(
            name="Morning Walk",
            description="Walk Max",
            duration_minutes=30,
            priority="high",
            frequency="daily"
        )
        
        # Initially, task should not be completed
        assert task.is_completed == False
        
        # Mark it complete
        task.mark_complete()
        
        # Now it should be completed
        assert task.is_completed == True

    def test_mark_incomplete(self):
        """Verify that marking a task incomplete changes its status."""
        task = Task(
            name="Feed Cat",
            description="Feed Whiskers",
            duration_minutes=10,
            priority="high",
            frequency="daily",
            is_completed=True
        )
        
        # Task starts as completed
        assert task.is_completed == True
        
        # Mark it incomplete
        task.mark_incomplete()
        
        # Now it should not be completed
        assert task.is_completed == False

    def test_is_due_today(self):
        """Verify that daily frequency tasks are recognized as due today."""
        daily_task = Task(
            name="Daily Task",
            description="Should be due today",
            duration_minutes=10,
            priority="medium",
            frequency="daily"
        )
        
        assert daily_task.is_due_today() == True

    def test_not_due_today(self):
        """Verify that weekly tasks are not marked as daily due."""
        weekly_task = Task(
            name="Weekly Task",
            description="Not due today",
            duration_minutes=20,
            priority="medium",
            frequency="weekly"
        )
        
        assert weekly_task.is_due_today() == False

    def test_priority_score(self):
        """Verify that priority strings map to correct numeric scores."""
        high_priority = Task("High", "desc", 10, priority="high", frequency="daily")
        medium_priority = Task("Medium", "desc", 10, priority="medium", frequency="daily")
        low_priority = Task("Low", "desc", 10, priority="low", frequency="daily")
        
        assert high_priority.get_priority_score() == 3
        assert medium_priority.get_priority_score() == 2
        assert low_priority.get_priority_score() == 1


class TestPet:
    """Test cases for the Pet class."""
    
    def test_add_task(self):
        """Verify that adding a task to a pet increases the task count."""
        pet = Pet(
            name="Max",
            species="Dog",
            age=3
        )
        
        # Initially, no tasks
        assert len(pet.tasks) == 0
        
        # Add a task
        task = Task(
            name="Walk",
            description="Morning walk",
            duration_minutes=30,
            priority="high",
            frequency="daily"
        )
        pet.add_task(task)
        
        # Now there should be one task
        assert len(pet.tasks) == 1
        assert pet.tasks[0].name == "Walk"

    def test_add_multiple_tasks(self):
        """Verify that multiple tasks can be added and are all stored."""
        pet = Pet(
            name="Whiskers",
            species="Cat",
            age=5
        )
        
        task1 = Task("Feed", "Feeding time", 10, "high", "daily")
        task2 = Task("Play", "Playtime", 15, "medium", "daily")
        task3 = Task("Groom", "Grooming", 20, "low", "weekly")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        assert len(pet.tasks) == 3

    def test_get_daily_tasks(self):
        """Verify that only daily tasks are returned."""
        pet = Pet(
            name="Max",
            species="Dog",
            age=3
        )
        
        daily_task = Task("Walk", "Walking", 30, "high", "daily")
        weekly_task = Task("Bath", "Bathing", 45, "low", "weekly")
        
        pet.add_task(daily_task)
        pet.add_task(weekly_task)
        
        daily_tasks = pet.get_daily_tasks()
        assert len(daily_tasks) == 1
        assert daily_tasks[0].name == "Walk"

    def test_get_total_task_duration(self):
        """Verify that task durations are summed correctly."""
        pet = Pet(
            name="Max",
            species="Dog",
            age=3
        )
        
        pet.add_task(Task("Walk", "Walking", 30, "high", "daily"))
        pet.add_task(Task("Feed", "Feeding", 10, "high", "daily"))
        pet.add_task(Task("Play", "Playing", 20, "medium", "daily"))
        
        assert pet.get_total_task_duration() == 60


class TestOwner:
    """Test cases for the Owner class."""
    
    def test_add_pet(self):
        """Verify that adding a pet increases the pet count."""
        owner = Owner(name="Sarah")
        
        assert len(owner.pets) == 0
        
        pet = Pet("Max", "Dog", 3)
        owner.add_pet(pet)
        
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Max"

    def test_get_total_available_minutes(self):
        """Verify that available minutes are calculated correctly."""
        owner = Owner(
            name="Sarah",
            availability_start=time(8, 0),
            availability_end=time(18, 0)
        )
        
        # 8 AM to 6 PM = 10 hours = 600 minutes
        assert owner.get_total_available_minutes() == 600

    def test_get_all_daily_tasks(self):
        """Verify that all daily tasks from all pets are retrieved."""
        owner = Owner(name="Sarah")
        
        dog = Pet("Max", "Dog", 3)
        cat = Pet("Whiskers", "Cat", 5)
        
        dog.add_task(Task("Walk", "Walking", 30, "high", "daily"))
        dog.add_task(Task("Feed", "Feeding", 10, "high", "daily"))
        
        cat.add_task(Task("Feed", "Feeding", 10, "high", "daily"))
        cat.add_task(Task("Bath", "Bathing", 45, "low", "weekly"))
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        all_daily_tasks = owner.get_all_daily_tasks()
        assert len(all_daily_tasks) == 3  # 2 from dog + 1 from cat

    def test_get_total_daily_task_minutes(self):
        """Verify that total minutes across all pets are summed correctly."""
        owner = Owner(name="Sarah")
        
        dog = Pet("Max", "Dog", 3)
        cat = Pet("Whiskers", "Cat", 5)
        
        dog.add_task(Task("Walk", "Walking", 30, "high", "daily"))
        dog.add_task(Task("Feed", "Feeding", 10, "high", "daily"))
        
        cat.add_task(Task("Feed", "Feeding", 10, "high", "daily"))
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        assert owner.get_total_daily_task_minutes() == 50


class TestScheduler:
    """Test cases for the Scheduler class."""
    
    def test_generate_schedule(self):
        """Verify that a schedule is generated with at least some tasks."""
        owner = Owner("Sarah", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        pet.add_task(Task("Walk", "Walking", 30, "high", "daily"))
        pet.add_task(Task("Feed", "Feeding", 10, "high", "daily"))
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        schedule = scheduler.generate_schedule()
        
        assert len(schedule) == 2
        assert schedule[0].task.name == "Walk"
        assert schedule[1].task.name == "Feed"

    def test_is_schedule_feasible(self):
        """Verify that feasibility is correctly evaluated."""
        owner = Owner("Sarah", time(8, 0), time(18, 0))  # 10 hours = 600 minutes
        pet = Pet("Max", "Dog", 3)
        pet.add_task(Task("Walk", "Walking", 30, "high", "daily"))
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        
        assert scheduler.is_schedule_feasible() == True

    def test_schedule_not_feasible(self):
        """Verify that infeasible schedules are detected."""
        owner = Owner("Sarah", time(8, 0), time(9, 0))  # 1 hour = 60 minutes
        pet = Pet("Max", "Dog", 3)
        # Add multiple high-priority tasks that won't fit
        pet.add_task(Task("Walk", "Walking", 45, "high", "daily"))
        pet.add_task(Task("Feed", "Feeding", 30, "high", "daily"))
        owner.add_pet(pet)
        
        scheduler = Scheduler(owner)
        
        assert scheduler.is_schedule_feasible() == False


class TestSorting:
    """Test cases for task sorting algorithms."""
    
    def test_sort_by_priority_high_first(self):
        """Verify that tasks are sorted with high priority first."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        # Add tasks in random priority order
        pet.add_task(Task("Low task", "Low priority", 10, "low", "daily"))
        pet.add_task(Task("High task", "High priority", 20, "high", "daily"))
        pet.add_task(Task("Medium task", "Medium priority", 15, "medium", "daily"))
        
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_tasks_by_priority(pet.get_daily_tasks())
        
        assert sorted_tasks[0].priority == "high"
        assert sorted_tasks[1].priority == "medium"
        assert sorted_tasks[2].priority == "low"

    def test_sort_by_duration_ascending(self):
        """Verify that tasks are sorted by duration (shortest first)."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        # Add tasks with different durations
        pet.add_task(Task("Task A", "30 min", 30, "medium", "daily"))
        pet.add_task(Task("Task B", "10 min", 10, "medium", "daily"))
        pet.add_task(Task("Task C", "20 min", 20, "medium", "daily"))
        
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_tasks_by_duration(pet.get_daily_tasks(), ascending=True)
        
        assert sorted_tasks[0].duration_minutes == 10
        assert sorted_tasks[1].duration_minutes == 20
        assert sorted_tasks[2].duration_minutes == 30

    def test_sort_by_duration_descending(self):
        """Verify that tasks can be sorted by duration (longest first)."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        pet.add_task(Task("Task A", "30 min", 30, "medium", "daily"))
        pet.add_task(Task("Task B", "10 min", 10, "medium", "daily"))
        pet.add_task(Task("Task C", "20 min", 20, "medium", "daily"))
        
        scheduler = Scheduler(owner)
        sorted_tasks = scheduler.sort_tasks_by_duration(pet.get_daily_tasks(), ascending=False)
        
        assert sorted_tasks[0].duration_minutes == 30
        assert sorted_tasks[1].duration_minutes == 20
        assert sorted_tasks[2].duration_minutes == 10


class TestFiltering:
    """Test cases for task filtering algorithms."""
    
    def test_filter_by_priority(self):
        """Verify that filtering by priority returns only matching tasks."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        pet.add_task(Task("Task 1", "High", 10, "high", "daily"))
        pet.add_task(Task("Task 2", "Low", 10, "low", "daily"))
        pet.add_task(Task("Task 3", "High", 10, "high", "daily"))
        pet.add_task(Task("Task 4", "Medium", 10, "medium", "daily"))
        
        scheduler = Scheduler(owner)
        all_tasks = pet.get_daily_tasks()
        high_priority = scheduler.filter_tasks_by_priority(all_tasks, "high")
        
        assert len(high_priority) == 2
        assert all(task.priority == "high" for task in high_priority)

    def test_filter_by_status_completed(self):
        """Verify that filtering by completion status works correctly."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        task1 = Task("Done", "Completed", 10, "high", "daily")
        task2 = Task("Pending", "Not done", 10, "high", "daily")
        task3 = Task("Also done", "Completed", 10, "high", "daily")
        
        task1.mark_complete()
        task3.mark_complete()
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        scheduler = Scheduler(owner)
        all_tasks = pet.get_daily_tasks()
        completed = scheduler.filter_tasks_by_status(all_tasks, completed=True)
        
        assert len(completed) == 2
        assert all(task.is_completed for task in completed)

    def test_filter_by_status_incomplete(self):
        """Verify that filtering for incomplete tasks works."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        task1 = Task("Done", "Completed", 10, "high", "daily")
        task2 = Task("Pending", "Not done", 10, "high", "daily")
        task3 = Task("Also pending", "Not done", 10, "high", "daily")
        
        task1.mark_complete()
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        scheduler = Scheduler(owner)
        all_tasks = pet.get_daily_tasks()
        incomplete = scheduler.filter_tasks_by_status(all_tasks, completed=False)
        
        assert len(incomplete) == 2
        assert all(not task.is_completed for task in incomplete)

    def test_search_tasks_by_name(self):
        """Verify that task search by name works correctly."""
        pet = Pet("Max", "Dog", 3)
        
        pet.add_task(Task("Morning walk", "Outdoor walk", 30, "high", "daily"))
        pet.add_task(Task("Evening walk", "Park time", 30, "high", "daily"))
        pet.add_task(Task("Feeding", "Dry kibble", 10, "high", "daily"))
        
        results = pet.search_tasks("walk")
        
        assert len(results) == 2
        assert all("walk" in task.name.lower() for task in results)

    def test_search_tasks_by_description(self):
        """Verify that task search by description works correctly."""
        pet = Pet("Max", "Dog", 3)
        
        pet.add_task(Task("Task 1", "Exercise activity", 30, "high", "daily"))
        pet.add_task(Task("Task 2", "Feeding activity", 10, "high", "daily"))
        pet.add_task(Task("Task 3", "Play activity", 20, "high", "daily"))
        
        results = pet.search_tasks("activity")
        
        assert len(results) == 3

    def test_search_tasks_case_insensitive(self):
        """Verify that task search is case-insensitive."""
        pet = Pet("Max", "Dog", 3)
        
        pet.add_task(Task("Morning Walk", "Outdoor time", 30, "high", "daily"))
        pet.add_task(Task("Feeding", "Dry kibble", 10, "high", "daily"))
        
        results_lower = pet.search_tasks("walk")
        results_upper = pet.search_tasks("WALK")
        results_mixed = pet.search_tasks("WaLk")
        
        assert len(results_lower) == len(results_upper) == len(results_mixed) == 1


class TestRecurringTasks:
    """Test cases for recurring task automation."""
    
    def test_mark_daily_task_creates_next_occurrence(self):
        """Verify that completing a daily task creates a new instance."""
        task = Task("Daily Feed", "Morning feeding", 10, "high", "daily")
        
        next_task = task.mark_complete()
        
        assert task.is_completed == True
        assert next_task is not None
        assert next_task.name == task.name
        assert next_task.is_completed == False
        assert next_task.frequency == "daily"

    def test_mark_weekly_task_creates_next_occurrence(self):
        """Verify that completing a weekly task creates a new instance."""
        task = Task("Weekly Bath", "Full bath", 45, "medium", "weekly")
        
        next_task = task.mark_complete()
        
        assert task.is_completed == True
        assert next_task is not None
        assert next_task.name == task.name
        assert next_task.frequency == "weekly"

    def test_non_recurring_task_returns_none(self):
        """Verify that non-recurring tasks return None when completed."""
        task = Task("One-time task", "Special task", 20, "high", "once")
        
        next_task = task.mark_complete()
        
        assert task.is_completed == True
        assert next_task is None

    def test_recurring_task_preserves_properties(self):
        """Verify that new recurring task instances preserve original properties."""
        original = Task(
            "Walk", 
            "Morning walk in park", 
            30, 
            priority="high", 
            frequency="daily"
        )
        
        next_task = original.mark_complete()
        
        assert next_task.name == original.name
        assert next_task.duration_minutes == original.duration_minutes
        assert next_task.priority == original.priority
        assert next_task.frequency == original.frequency
        assert next_task.description == original.description

    def test_adding_recurring_task_to_pet(self):
        """Verify that recurring task can be added to pet after completion."""
        pet = Pet("Max", "Dog", 3)
        task = Task("Feed Max", "Daily feeding", 10, "high", "daily")
        
        pet.add_task(task)
        assert len(pet.tasks) == 1
        
        next_task = task.mark_complete()
        pet.add_task(next_task)
        
        assert len(pet.tasks) == 2
        assert pet.tasks[0].is_completed == True
        assert pet.tasks[1].is_completed == False


class TestConflictDetection:
    """Test cases for task conflict detection."""
    
    def test_no_conflicts_in_sequential_schedule(self):
        """Verify that sequential tasks have no conflicts."""
        owner = Owner("Test", time(8, 0), time(18, 0))
        pet = Pet("Max", "Dog", 3)
        
        pet.add_task(Task("Task 1", "First", 30, "high", "daily"))
        pet.add_task(Task("Task 2", "Second", 20, "high", "daily"))
        
        scheduler = Scheduler(owner)
        scheduler.generate_schedule()
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 0

    def test_detect_overlapping_tasks(self):
        """Verify that overlapping tasks are detected."""
        scheduler = Scheduler(Owner("Test", time(8, 0), time(18, 0)))
        
        task1 = Task("Task A", "First task", 30, "high", "daily")
        task2 = Task("Task B", "Second task", 30, "high", "daily")
        
        # Manually create overlapping schedule
        scheduler.schedule = [
            ScheduledTask(task1, time(9, 0), 30),   # 9:00-9:30
            ScheduledTask(task2, time(9, 15), 30),  # 9:15-9:45 (overlaps)
        ]
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 1

    def test_detect_exact_time_overlap(self):
        """Verify that tasks at exact same time are detected."""
        scheduler = Scheduler(Owner("Test", time(8, 0), time(18, 0)))
        
        task1 = Task("Task A", "First", 30, "high", "daily")
        task2 = Task("Task B", "Second", 30, "high", "daily")
        
        # Both start at same time
        scheduler.schedule = [
            ScheduledTask(task1, time(10, 0), 30),
            ScheduledTask(task2, time(10, 0), 30),
        ]
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 1

    def test_adjacent_tasks_no_conflict(self):
        """Verify that adjacent tasks (back-to-back) don't conflict."""
        scheduler = Scheduler(Owner("Test", time(8, 0), time(18, 0)))
        
        task1 = Task("Task A", "First", 30, "high", "daily")
        task2 = Task("Task B", "Second", 30, "high", "daily")
        
        # Task 1: 9:00-9:30, Task 2: 9:30-10:00 (no overlap)
        scheduler.schedule = [
            ScheduledTask(task1, time(9, 0), 30),
            ScheduledTask(task2, time(9, 30), 30),
        ]
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) == 0

    def test_conflicts_summary_message(self):
        """Verify that conflict summary generates readable message."""
        scheduler = Scheduler(Owner("Test", time(8, 0), time(18, 0)))
        
        task1 = Task("Walk", "Outdoor", 30, "high", "daily")
        task2 = Task("Feed", "Food time", 30, "high", "daily")
        
        scheduler.schedule = [
            ScheduledTask(task1, time(10, 0), 30),
            ScheduledTask(task2, time(10, 15), 30),
        ]
        
        summary = scheduler.get_conflicts_summary()
        
        assert "CONFLICT DETECTED" in summary
        assert "Walk" in summary
        assert "Feed" in summary

    def test_no_conflicts_summary_message(self):
        """Verify that no conflicts returns positive message."""
        scheduler = Scheduler(Owner("Test", time(8, 0), time(18, 0)))
        
        task1 = Task("Task A", "First", 30, "high", "daily")
        scheduler.schedule = [ScheduledTask(task1, time(10, 0), 30)]
        
        summary = scheduler.get_conflicts_summary()
        
        assert "No scheduling conflicts" in summary


class TestAdvancedQuerying:
    """Test cases for advanced Owner and Pet querying capabilities."""
    
    def test_get_pet_by_name(self):
        """Verify that pets can be found by name."""
        owner = Owner("Test")
        
        dog = Pet("Max", "Dog", 3)
        cat = Pet("Whiskers", "Cat", 5)
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        found = owner.get_pet_by_name("Max")
        assert found is not None
        assert found.name == "Max"
        assert found.species == "Dog"

    def test_get_pet_by_name_case_insensitive(self):
        """Verify that pet search is case-insensitive."""
        owner = Owner("Test")
        owner.add_pet(Pet("Max", "Dog", 3))
        
        found_lower = owner.get_pet_by_name("max")
        found_upper = owner.get_pet_by_name("MAX")
        found_mixed = owner.get_pet_by_name("MaX")
        
        assert found_lower is not None
        assert found_upper is not None
        assert found_mixed is not None

    def test_get_pet_by_name_not_found(self):
        """Verify that searching for non-existent pet returns None."""
        owner = Owner("Test")
        owner.add_pet(Pet("Max", "Dog", 3))
        
        not_found = owner.get_pet_by_name("Buddy")
        assert not_found is None

    def test_get_high_priority_tasks_all_pets(self):
        """Verify that high-priority tasks are aggregated across all pets."""
        owner = Owner("Test")
        
        dog = Pet("Max", "Dog", 3)
        dog.add_task(Task("Walk", "High task", 30, "high", "daily"))
        dog.add_task(Task("Play", "Low task", 20, "low", "daily"))
        
        cat = Pet("Whiskers", "Cat", 5)
        cat.add_task(Task("Feed", "High task", 10, "high", "daily"))
        cat.add_task(Task("Groom", "Medium task", 15, "medium", "daily"))
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        high_priority = owner.get_all_high_priority_tasks()
        
        assert len(high_priority) == 2
        assert all(task.priority == "high" for task in high_priority)

    def test_get_incomplete_tasks_by_pet(self):
        """Verify that incomplete tasks are grouped by pet."""
        owner = Owner("Test")
        
        dog = Pet("Max", "Dog", 3)
        cat = Pet("Whiskers", "Cat", 5)
        
        dog_task1 = Task("Walk", "Outdoor", 30, "high", "daily")
        dog_task2 = Task("Feed", "Food", 10, "high", "daily")
        dog_task2.mark_complete()
        
        cat_task1 = Task("Feed", "Food", 10, "high", "daily")
        
        dog.add_task(dog_task1)
        dog.add_task(dog_task2)
        cat.add_task(cat_task1)
        
        owner.add_pet(dog)
        owner.add_pet(cat)
        
        incomplete = owner.get_incomplete_tasks_by_pet()
        
        assert "Max" in incomplete
        assert "Whiskers" in incomplete
        assert len(incomplete["Max"]) == 1
        assert len(incomplete["Whiskers"]) == 1
