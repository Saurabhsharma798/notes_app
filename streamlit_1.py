import streamlit_1 as st


def toggle_done(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]

st.set_page_config(page_title="To-Do App", layout="centered")

st.title("📝 To-Do List")

# Session state to hold tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add new task
new_task = st.text_input("Add a task", placeholder="Buy groceries...")

if st.button("Add Task"):
    if new_task:
        st.session_state.tasks.append({"task": new_task, "done": False})
        st.success("Task added!")
    else:
        st.warning("Task cannot be empty.")

# Display and update tasks
for i, task in enumerate(st.session_state.tasks):
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
    with col1:
        st.checkbox(task["task"], key=f"done_{i}", value=task["done"],
                    on_change=lambda i=i: toggle_done(i))
    with col2:
        if st.button("✅", key=f"mark_{i}"):
            toggle_done(i)
    with col3:
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()

   