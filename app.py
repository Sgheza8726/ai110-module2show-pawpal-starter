import streamlit as st
from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, your pet care planning assistant!

This app helps you organize daily pet care tasks, set priorities, and generate optimized schedules.
"""
)

st.divider()

# ============================================================================
# Session State Management - Initialize Owner and Pets on First Load
# ============================================================================

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Your Name")

if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None


# ============================================================================
# Sidebar: Owner Information & Pet Management
# ============================================================================

with st.sidebar:
    st.subheader("👤 Owner Profile")
    
    owner_name = st.text_input(
        "Your name",
        value=st.session_state.owner.name,
        key="owner_name_input"
    )
    st.session_state.owner.name = owner_name
    
    col1, col2 = st.columns(2)
    with col1:
        start_hour = st.slider(
            "Day starts at",
            min_value=0,
            max_value=23,
            value=st.session_state.owner.availability_start.hour,
            key="start_hour"
        )
    with col2:
        start_minute = st.slider(
            "Minutes",
            min_value=0,
            max_value=59,
            value=st.session_state.owner.availability_start.minute,
            step=15,
            key="start_minute"
        )
    st.session_state.owner.availability_start = time(start_hour, start_minute)
    
    col1, col2 = st.columns(2)
    with col1:
        end_hour = st.slider(
            "Day ends at",
            min_value=0,
            max_value=23,
            value=st.session_state.owner.availability_end.hour,
            key="end_hour"
        )
    with col2:
        end_minute = st.slider(
            "Minutes",
            min_value=0,
            max_value=59,
            value=st.session_state.owner.availability_end.minute,
            step=15,
            key="end_minute"
        )
    st.session_state.owner.availability_end = time(end_hour, end_minute)
    
    st.divider()
    
    st.subheader("🐾 Pets")
    st.caption(f"Managing {len(st.session_state.owner.pets)} pet(s)")
    
    # Display existing pets
    if st.session_state.owner.pets:
        for pet in st.session_state.owner.pets:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📍 {pet.name} ({pet.species})", key=f"pet_{pet.name}"):
                    st.session_state.selected_pet = pet
            with col2:
                if st.button("✕", key=f"delete_{pet.name}"):
                    st.session_state.owner.pets.remove(pet)
                    st.session_state.selected_pet = None
                    st.rerun()
    else:
        st.info("No pets yet. Add one below.")
    
    st.divider()
    st.subheader("➕ Add New Pet")
    
    new_pet_name = st.text_input("Pet name", key="new_pet_name")
    new_pet_species = st.selectbox("Species", ["dog", "cat", "rabbit", "bird", "hamster", "other"], key="new_pet_species")
    new_pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=1, key="new_pet_age")
    new_pet_needs = st.text_area("Special needs (optional)", key="new_pet_needs")
    
    if st.button("Add Pet", key="add_pet_btn", use_container_width=True):
        if new_pet_name.strip():
            new_pet = Pet(
                name=new_pet_name,
                species=new_pet_species,
                age=int(new_pet_age),
                special_needs=new_pet_needs
            )
            st.session_state.owner.add_pet(new_pet)
            st.session_state.selected_pet = new_pet
            st.rerun()
        else:
            st.error("Please enter a pet name.")


# ============================================================================
# Main Content: Task Management & Scheduling
# ============================================================================

if st.session_state.selected_pet is None:
    st.info("👈 Select a pet from the sidebar to get started, or add a new pet!")
    
    # Show overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pets", len(st.session_state.owner.pets))
    with col2:
        total_tasks = sum(len(pet.tasks) for pet in st.session_state.owner.pets)
        st.metric("Total Tasks", total_tasks)
    with col3:
        total_minutes = st.session_state.owner.get_total_daily_task_minutes()
        hours = total_minutes // 60
        mins = total_minutes % 60
        st.metric("Daily Time", f"{hours}h {mins}m")

else:
    pet = st.session_state.selected_pet
    
    st.subheader(f"🐾 {pet.name} ({pet.species})")
    st.caption(f"Age: {pet.age} years | Special needs: {pet.special_needs if pet.special_needs else 'None'}")
    
    # ========== Task Management ==========
    st.divider()
    st.subheader(f"📋 Tasks for {pet.name}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_name = st.text_input("Task name", placeholder="e.g., Morning walk", key="task_name")
    with col2:
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=30, key="task_duration")
    with col3:
        task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="task_priority")
    with col4:
        task_frequency = st.selectbox("Frequency", ["daily", "twice-daily", "weekly"], key="task_frequency")
    
    if st.button("Add Task", use_container_width=False):
        if task_name.strip():
            new_task = Task(
                name=task_name,
                description=f"Task for {pet.name}",
                duration_minutes=int(task_duration),
                priority=task_priority,
                frequency=task_frequency
            )
            pet.add_task(new_task)
            st.rerun()
        else:
            st.error("Please enter a task name.")
    
    # Display tasks
    if pet.tasks:
        st.write("**Current Tasks:**")
        for idx, task in enumerate(pet.tasks):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
            with col1:
                st.text(task.name)
            with col2:
                priority_badge = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                st.text(f"{priority_badge.get(task.priority, '○')} {task.priority}")
            with col3:
                st.text(f"{task.duration_minutes} min")
            with col4:
                st.text(task.frequency)
            with col5:
                if st.button("🗑", key=f"delete_task_{idx}"):
                    pet.tasks.pop(idx)
                    st.rerun()
    else:
        st.info(f"No tasks for {pet.name} yet. Add one above!")
    
    # ========== Schedule Generation ==========
    st.divider()
    st.subheader("📅 Generate Daily Schedule")
    
    col1, col2 = st.columns(2)
    with col1:
        available_minutes = st.session_state.owner.get_total_available_minutes()
        available_hours = available_minutes // 60
        available_mins = available_minutes % 60
        st.metric(
            "Owner Availability",
            f"{st.session_state.owner.availability_start.strftime('%H:%M')} - {st.session_state.owner.availability_end.strftime('%H:%M')}",
            f"{available_hours}h {available_mins}m"
        )
    with col2:
        daily_minutes = st.session_state.owner.get_total_daily_task_minutes()
        daily_hours = daily_minutes // 60
        daily_mins = daily_minutes % 60
        st.metric(
            "Total Daily Tasks",
            f"{len(st.session_state.owner.get_all_daily_tasks())} tasks",
            f"{daily_hours}h {daily_mins}m"
        )
    
    if st.button("🚀 Generate Schedule", use_container_width=True):
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.generate_schedule()
        
        if schedule:
            st.success("Schedule generated successfully!")
            st.write(scheduler.get_schedule_summary())
            
            # Detailed schedule view
            st.subheader("Detailed Schedule")
            schedule_data = []
            for scheduled_task in schedule:
                end_time = scheduled_task.get_end_time()
                schedule_data.append({
                    "Time": f"{scheduled_task.scheduled_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}",
                    "Task": scheduled_task.task.name,
                    "Pet": "TBD",  # Could be enhanced to track which pet
                    "Duration": f"{scheduled_task.duration_minutes} min",
                    "Priority": scheduled_task.task.priority
                })
            
            st.dataframe(schedule_data, use_container_width=True)
            
            # Feasibility check
            if scheduler.is_schedule_feasible():
                st.success("✓ All high-priority tasks fit in your schedule!")
            else:
                st.warning("⚠️ Not all high-priority tasks could be scheduled. Consider adjusting availability or removing low-priority tasks.")
        else:
            st.warning("No tasks to schedule. Add tasks to your pets first.")
