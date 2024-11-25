import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store the tasks
TASK_FILE = 'todo.json'

# Load tasks from the JSON file
def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    with open(TASK_FILE, 'r') as file:
        return json.load(file)

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Add a task to the list
def add_task():
    task = task_entry.get()
    if task.strip():
        tasks.append(task)
        save_tasks(tasks)
        update_task_listbox()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Task cannot be empty!")

# Delete a selected task
def delete_task():
    try:
        selected_index = task_listbox.curselection()[0]
        task = tasks.pop(selected_index)
        save_tasks(tasks)
        update_task_listbox()
        messagebox.showinfo("Task Deleted", f"Task '{task}' has been deleted.")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

# Update a selected task
def update_task():
    try:
        selected_index = task_listbox.curselection()[0]
        task = tasks[selected_index]
        new_task = task_entry.get()
        if new_task.strip():
            tasks[selected_index] = new_task
            save_tasks(tasks)
            update_task_listbox()
            task_entry.delete(0, tk.END)
            messagebox.showinfo("Task Updated", f"Task '{task}' updated to '{new_task}'.")
        else:
            messagebox.showwarning("Input Error", "Updated task cannot be empty!")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to update.")

# Update the listbox to display current tasks
def update_task_listbox():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

# Initialize the GUI
def init_gui():
    global task_entry, task_listbox

    # Create the main window
    window = tk.Tk()
    window.title("To-Do List App")
    window.geometry("400x500")

    # Task input
    tk.Label(window, text="Enter Task:").pack(pady=5)
    task_entry = tk.Entry(window, width=40)
    task_entry.pack(pady=5)

    # Buttons
    tk.Button(window, text="Add Task", command=add_task).pack(pady=5)
    tk.Button(window, text="Update Task", command=update_task).pack(pady=5)
    tk.Button(window, text="Delete Task", command=delete_task).pack(pady=5)

    # Task List
    tk.Label(window, text="Tasks:").pack(pady=10)
    task_listbox_frame = tk.Frame(window)
    task_listbox_frame.pack(pady=5)

    scrollbar = tk.Scrollbar(task_listbox_frame, orient=tk.VERTICAL)
    task_listbox = tk.Listbox(
        task_listbox_frame, width=40, height=15, yscrollcommand=scrollbar.set
    )
    scrollbar.config(command=task_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    # Populate listbox with saved tasks
    update_task_listbox()

    # Start the GUI loop
    window.mainloop()

if __name__ == '__main__':
    tasks = load_tasks()
    init_gui()
