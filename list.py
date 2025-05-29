import streamlit as st

# Initialize session state for tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

st.set_page_config(page_title="To-do list app", page_icon="✔", layout="centered" )
# Function to add a task
def add_task(task):
    if task:
        st.session_state.tasks.append(task)

# Function to remove a task
def remove_task(index):
    if 0 <= index < len(st.session_state.tasks):
        st.session_state.tasks.pop(index)

# Streamlit UI
st.title("To-Do List App")

# Input box for new task
new_task = st.text_input("Enter a new task:")

# Button to add the task
if st.button("Add Task"):
    add_task(new_task)

# Display the current tasks
if st.session_state.tasks:
    st.subheader("Your Tasks:")
    for index, task in enumerate(st.session_state.tasks):
        task_label = f"{index + 1}. {task}"
        col1, col2 = st.columns([8, 1])
        with col1:
            st.write(task_label)
        with col2:
            if st.button("Remove", key=index):
                remove_task(index)

# Footer
st.write("Made with ❤️ from Grey code")
