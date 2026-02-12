"""
Tests for PawPal+ System

This module contains unit tests for the core PawPal+ functionality.
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler
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
