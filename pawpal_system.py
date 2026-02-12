"""
PawPal+ System Logic Layer

This module contains the core classes that make up the PawPal+ system:
- Owner: Represents the pet owner
- Pet: Represents an individual pet
- Task: Represents a pet care task
- Scheduler: Generates daily schedules based on tasks and constraints
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, time


@dataclass
class Task:
    """
    Represents a pet care task.
    
    Attributes:
        name (str): Task name (e.g., "Morning walk")
        description (str): Detailed description
        duration_minutes (int): How long the task takes
        priority (str): One of 'high', 'medium', 'low'
        frequency (str): How often (e.g., 'daily', 'twice-daily', 'weekly')
        is_completed (bool): Whether the task has been done today
    """
    name: str
    description: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "daily"
    is_completed: bool = False

    def is_due_today(self) -> bool:
        """Determine if this task should be done today based on frequency."""
        daily_frequencies = ['daily', 'twice-daily', 'three-times-daily']
        return self.frequency in daily_frequencies

    def get_priority_score(self) -> int:
        """Convert priority string to numeric score for scheduling."""
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        return priority_map.get(self.priority, 2)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as incomplete."""
        self.is_completed = False


@dataclass
class Pet:
    """
    Represents a pet.
    
    Attributes:
        name (str): Pet's name
        species (str): Type of pet (dog, cat, rabbit, etc.)
        age (int): Age in years
        special_needs (str): Any special care requirements
        tasks (List[Task]): List of care tasks for this pet
    """
    name: str
    species: str
    age: int
    special_needs: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        self.tasks.append(task)

    def get_daily_tasks(self) -> List[Task]:
        """Return all tasks that should happen today."""
        return [task for task in self.tasks if task.is_due_today()]

    def get_total_task_duration(self) -> int:
        """Sum the duration of all daily tasks in minutes."""
        return sum(task.duration_minutes for task in self.get_daily_tasks())

    def get_incomplete_tasks(self) -> List[Task]:
        """Return all daily tasks that haven't been completed yet."""
        return [task for task in self.get_daily_tasks() if not task.is_completed]


@dataclass
class Owner:
    """
    Represents a pet owner.
    
    Attributes:
        name (str): Owner's name
        availability_start (time): When the owner's day starts (e.g., 8:00 AM)
        availability_end (time): When the owner's day ends (e.g., 10:00 PM)
        preferences (dict): Owner's preferences for scheduling
        pets (List[Pet]): List of pets owned
    """
    name: str
    availability_start: time = field(default_factory=lambda: time(8, 0))
    availability_end: time = field(default_factory=lambda: time(22, 0))
    preferences: dict = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's list."""
        self.pets.append(pet)

    def get_total_available_minutes(self) -> int:
        """Calculate total minutes available in a day."""
        start_minutes = self.availability_start.hour * 60 + self.availability_start.minute
        end_minutes = self.availability_end.hour * 60 + self.availability_end.minute
        return end_minutes - start_minutes

    def update_preferences(self, new_preferences: dict) -> None:
        """Update scheduling preferences."""
        self.preferences.update(new_preferences)

    def get_all_daily_tasks(self) -> List[Task]:
        """Retrieve all daily tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_daily_tasks())
        return all_tasks

    def get_total_daily_task_minutes(self) -> int:
        """Sum the duration of all daily tasks across all pets."""
        return sum(pet.get_total_task_duration() for pet in self.pets)


class ScheduledTask:
    """
    Represents a task scheduled at a specific time.
    
    Attributes:
        task (Task): The task being scheduled
        scheduled_time (time): When it should happen
        duration_minutes (int): How long it will take
    """
    def __init__(self, task: Task, scheduled_time: time, duration_minutes: int):
        self.task = task
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes

    def get_end_time(self) -> time:
        """Calculate when this task will finish."""
        total_minutes = (self.scheduled_time.hour * 60 + 
                        self.scheduled_time.minute + 
                        self.duration_minutes)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return time(hours % 24, minutes)

    def overlaps_with(self, other: 'ScheduledTask') -> bool:
        """Check if this task overlaps with another."""
        self_start = self.scheduled_time.hour * 60 + self.scheduled_time.minute
        self_end = self_start + self.duration_minutes
        
        other_start = other.scheduled_time.hour * 60 + other.scheduled_time.minute
        other_end = other_start + other.duration_minutes
        
        return not (self_end <= other_start or other_end <= self_start)

    def __str__(self) -> str:
        """Return a readable string representation."""
        end_time = self.get_end_time()
        return f"{self.scheduled_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}: {self.task.name} ({self.duration_minutes} min)"


class Scheduler:
    """
    Generates an optimized daily schedule.
    
    The scheduler takes an owner's pets and their tasks, then arranges them
    into a feasible daily plan that respects time constraints and prioritizes
    high-importance tasks.
    
    Attributes:
        owner (Owner): The owner whose schedule is being planned
        schedule (List[ScheduledTask]): The planned tasks for the day
    """
    def __init__(self, owner: Owner):
        self.owner = owner
        self.schedule: List[ScheduledTask] = []

    def generate_schedule(self) -> List[ScheduledTask]:
        """
        Create a daily schedule for all pets.
        
        Sorts tasks by priority (high first), then fits them into available time slots
        starting from the owner's availability start time.
        
        Returns:
            A list of ScheduledTask objects representing today's plan.
        """
        # Get all daily tasks and sort by priority (descending)
        all_tasks = self.owner.get_all_daily_tasks()
        all_tasks.sort(key=lambda t: t.get_priority_score(), reverse=True)
        
        self.schedule = []
        current_time = self.owner.availability_start
        
        for task in all_tasks:
            # Check if task fits before owner's availability ends
            task_end_minutes = (current_time.hour * 60 + current_time.minute + task.duration_minutes)
            availability_end_minutes = (self.owner.availability_end.hour * 60 + 
                                       self.owner.availability_end.minute)
            
            if task_end_minutes <= availability_end_minutes:
                scheduled = ScheduledTask(task, current_time, task.duration_minutes)
                self.schedule.append(scheduled)
                # Update current time for next task
                current_time = scheduled.get_end_time()
        
        return self.schedule

    def can_fit_task(self, task: Task, proposed_time: time) -> bool:
        """Check if a task can fit at a proposed time without conflicts."""
        proposed_minutes = proposed_time.hour * 60 + proposed_time.minute
        task_end_minutes = proposed_minutes + task.duration_minutes
        availability_end_minutes = (self.owner.availability_end.hour * 60 + 
                                   self.owner.availability_end.minute)
        
        if task_end_minutes > availability_end_minutes:
            return False
        
        # Check for overlaps with existing scheduled tasks
        for scheduled in self.schedule:
            test_scheduled = ScheduledTask(task, proposed_time, task.duration_minutes)
            if test_scheduled.overlaps_with(scheduled):
                return False
        
        return True

    def get_schedule_summary(self) -> str:
        """Return a human-readable summary of today's schedule."""
        if not self.schedule:
            return "No tasks scheduled for today."
        
        summary = f"Today's Schedule for {self.owner.name}:\n"
        summary += "-" * 50 + "\n"
        for scheduled_task in self.schedule:
            summary += f"  {scheduled_task}\n"
        summary += "-" * 50 + "\n"
        
        total_minutes = sum(st.duration_minutes for st in self.schedule)
        summary += f"Total time: {total_minutes} minutes ({total_minutes // 60}h {total_minutes % 60}m)"
        
        return summary

    def is_schedule_feasible(self) -> bool:
        """Verify that all critical tasks fit within available time."""
        total_time_needed = 0
        critical_tasks = [t for t in self.owner.get_all_daily_tasks() 
                         if t.priority == 'high']
        
        for task in critical_tasks:
            total_time_needed += task.duration_minutes
        
        available_time = self.owner.get_total_available_minutes()
        return total_time_needed <= available_time
