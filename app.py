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
        
        # Task display and filtering options
        col1, col2, col3 = st.columns(3)
        with col1:
            task_filter_mode = st.radio("Filter View", ["All Tasks", "By Priority", "By Status", "Search"], horizontal=True)
        
        scheduler = Scheduler(st.session_state.owner)
        
        if task_filter_mode == "All Tasks":
            # Show all tasks in a table format
            display_tasks = pet.get_daily_tasks()
        elif task_filter_mode == "By Priority":
            selected_priority = st.selectbox("Select Priority", ["high", "medium", "low"], key="priority_filter")
            display_tasks = scheduler.filter_tasks_by_priority(pet.get_daily_tasks(), selected_priority)
        elif task_filter_mode == "By Status":
            status_choice = st.radio("Completion Status", ["Incomplete", "Completed"], horizontal=True)
            completed = (status_choice == "Completed")
            display_tasks = scheduler.filter_tasks_by_status(pet.get_daily_tasks(), completed=completed)
        else:  # Search
            search_query = st.text_input("🔍 Search tasks by name or description", key="task_search")
            display_tasks = pet.search_tasks(search_query) if search_query else pet.get_daily_tasks()
        
        # Display filtered/sorted tasks with better formatting
        if display_tasks:
            task_df_data = []
            for task in display_tasks:
                priority_badge = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                task_df_data.append({
                    "Task": task.name,
                    "Priority": f"{priority_badge.get(task.priority, '○')} {task.priority}",
                    "Duration": f"{task.duration_minutes} min",
                    "Frequency": task.frequency,
                    "Status": "✓ Done" if task.is_completed else "⏳ Pending"
                })
            
            st.dataframe(task_df_data, use_container_width=True, hide_index=True)
            
            # Show sorting options
            with st.expander("📊 Sort Tasks", expanded=False):
                sort_option = st.selectbox("Sort by:", ["Priority (High First)", "Duration (Short First)", "Duration (Long First)"], key="sort_select")
                
                if sort_option == "Priority (High First)":
                    sorted_tasks = scheduler.sort_tasks_by_priority(display_tasks)
                elif sort_option == "Duration (Short First)":
                    sorted_tasks = scheduler.sort_tasks_by_duration(display_tasks, ascending=True)
                else:  # Long first
                    sorted_tasks = scheduler.sort_tasks_by_duration(display_tasks, ascending=False)
                
                st.write("**Sorted Task Order:**")
                for i, task in enumerate(sorted_tasks, 1):
                    st.text(f"{i}. {task.name} ({task.duration_minutes} min, {task.priority} priority)")
        else:
            st.info("No tasks matching your filter.")
        
        # Task management interface
        st.divider()
        st.subheader("➕ Manage Individual Tasks")
        
        if display_tasks:
            task_to_manage = st.selectbox("Select a task to manage:", [t.name for t in pet.get_daily_tasks()], key="task_manage_select")
            task_to_manage_obj = next((t for t in pet.get_daily_tasks() if t.name == task_to_manage), None)
            
            if task_to_manage_obj:
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("✓ Mark Complete", key="mark_complete_btn"):
                        next_task = task_to_manage_obj.mark_complete()
                        if next_task:
                            pet.add_task(next_task)
                            st.success(f"✓ Marked '{task_to_manage}' complete! New recurring instance created.")
                        else:
                            st.success(f"✓ Marked '{task_to_manage}' complete!")
                        st.rerun()
                with col2:
                    if st.button("✕ Delete Task", key="delete_manage_btn"):
                        pet.tasks.remove(task_to_manage_obj)
                        st.success(f"Deleted '{task_to_manage}'")
                        st.rerun()
                with col3:
                    if task_to_manage_obj.is_completed:
                        if st.button("↺ Mark Incomplete", key="mark_incomplete_btn"):
                            task_to_manage_obj.mark_incomplete()
                            st.info(f"Marked '{task_to_manage}' as incomplete")
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
            st.success("✓ Schedule generated successfully!")
            
            # Display summary
            st.write(scheduler.get_schedule_summary())
            
            # Conflict detection
            st.divider()
            st.subheader("⚠️ Conflict Detection")
            conflict_summary = scheduler.get_conflicts_summary()
            if "No scheduling conflicts" in conflict_summary:
                st.success(conflict_summary)
            else:
                st.warning(conflict_summary)
            
            # Detailed schedule view
            st.divider()
            st.subheader("📅 Detailed Schedule")
            schedule_data = []
            for scheduled_task in schedule:
                end_time = scheduled_task.get_end_time()
                schedule_data.append({
                    "Time": f"{scheduled_task.scheduled_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}",
                    "Task": scheduled_task.task.name,
                    "Duration": f"{scheduled_task.duration_minutes} min",
                    "Priority": scheduled_task.task.priority.upper(),
                    "Frequency": scheduled_task.task.frequency
                })
            
            st.dataframe(schedule_data, use_container_width=True, hide_index=True)
            
            # Feasibility check
            st.divider()
            st.subheader("📊 Schedule Analysis")
            col1, col2, col3 = st.columns(3)
            with col1:
                total_scheduled = sum(st.duration_minutes for st in schedule)
                st.metric("Scheduled Time", f"{total_scheduled} min")
            with col2:
                available_minutes = st.session_state.owner.get_total_available_minutes()
                st.metric("Available Time", f"{available_minutes} min")
            with col3:
                utilization = (total_scheduled / available_minutes * 100) if available_minutes > 0 else 0
                st.metric("Utilization", f"{utilization:.1f}%")
            
            # Feasibility and high-priority task analysis
            st.divider()
            if scheduler.is_schedule_feasible():
                st.success("✓ Schedule is feasible - all high-priority tasks fit in your available time!")
            else:
                st.warning("⚠️ Not all high-priority tasks could be scheduled. Consider adjusting owner availability or removing low-priority tasks.")
            
            # High priority task summary
            high_priority_tasks = st.session_state.owner.get_all_high_priority_tasks()
            scheduled_high_priority = [st.task for st in schedule if st.task.priority == "high"]
            
            if high_priority_tasks:
                st.info(f"**High-Priority Tasks**: {len(scheduled_high_priority)}/{len(high_priority_tasks)} scheduled")
                if len(scheduled_high_priority) < len(high_priority_tasks):
                    missed = [t.name for t in high_priority_tasks if t not in scheduled_high_priority]
                    st.caption(f"Could not schedule: {', '.join(missed)}")
        else:
            st.warning("No tasks to schedule. Add tasks to your pets first.")
