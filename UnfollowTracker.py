import tkinter as tk
from tkinter import messagebox
import threading
import requests

# ------------------------------------------------------
# GitHub credentials (Replace with your own credentials)
# ------------------------------------------------------
GITHUB_TOKEN = "your-github-token-here"  # GitHub Personal Access Token
USERNAME = "your-username-here"  # GitHub Username

# ------------------------------------------------------
# Authorization headers for GitHub API
# ------------------------------------------------------
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"  # Set the authorization header for API requests
}

# ------------------------------------------------------
# Helper function to retrieve paginated data from GitHub
# ------------------------------------------------------
def get_all(url):
    """
    Fetches all paginated results from a given GitHub API URL.
    This function follows pagination links to retrieve all data.
    """
    results = []
    while url:
        response = requests.get(url, headers=headers)  # Send GET request to GitHub API
        response.raise_for_status()  # Raise an exception for invalid responses (non-2xx)
        results += response.json()  # Add the current page results to the list
        url = response.links.get('next', {}).get('url')  # Get the URL for the next page if available
    return results

# ------------------------------------------------------
# Unfollow a specific GitHub user
# ------------------------------------------------------
def unfollow_user(user):
    """
    Sends a DELETE request to GitHub's API to unfollow a specific user.
    Returns True if the unfollow request is successful (HTTP 204), False otherwise.
    """
    url = f"https://api.github.com/user/following/{user}"  # API URL for unfollowing a user
    response = requests.delete(url, headers=headers)  # Send DELETE request
    return response.status_code == 204  # Return True if the status code is 204 (No Content)

# ------------------------------------------------------
# GUI Setup and Utility Functions
# ------------------------------------------------------
def switch_theme():
    """
    Toggles between light and dark themes for the application.
    """
    global is_dark_mode
    is_dark_mode = not is_dark_mode  # Toggle the theme mode
    apply_theme()  # Apply the updated theme

def apply_theme():
    """
    Applies the selected theme (dark or light) to the application’s UI elements.
    """
    bg = "#2b2b2b" if is_dark_mode else "#ffffff"  # Background color for the theme
    fg = "white" if is_dark_mode else "black"  # Foreground color for text
    box_bg = "#3c3f41" if is_dark_mode else "#f0f0f0"  # Background color for input fields
    box_fg = "#add8e6" if is_dark_mode else "black"  # Text color for input fields

    # Apply the theme to window and components
    window.configure(bg=bg)
    stats_frame.configure(bg=bg)
    button_frame.configure(bg=bg)
    container.config(bg=bg)
    canvas.config(bg=box_bg)
    scrollable_frame.config(bg=box_bg)

    # Update the text color for the labels
    for label in stats_labels:
        label.config(bg=bg, fg=fg)

    # Apply the theme to entry fields and checkboxes
    for frame, entry, cb in entry_rows:
        frame.config(bg=box_bg)
        entry.config(readonlybackground=box_bg, fg=box_fg)
        cb.config(bg=box_bg, activebackground=box_bg)

    # Customize the button styles based on the theme
    select_all_cb.config(bg=box_bg, activebackground=box_bg, fg=box_fg)
    submit_btn.config(bg="#4caf50", fg="white", activebackground="#45a049")
    theme_btn.config(bg="#555555" if is_dark_mode else "#dddddd", fg="white" if is_dark_mode else "black")
    refresh_btn.config(bg="#2196F3", fg="white")

def show_selected():
    """
    Unfollows the users selected in the checkboxes and shows the result.
    Displays a message indicating how many users were successfully unfollowed.
    """
    set_loading(True)  # Start the loading indicator

    selected = [var.get() for var in checkbox_vars if var.get()]  # Get list of selected users
    if selected:
        successful, failed = [], []
        for user in selected:
            if unfollow_user(user):  # Try to unfollow the user
                successful.append(user)
            else:
                failed.append(user)

        # Show the result summary in a message box
        msg = ""
        if successful:
            msg += f"\u2705 Successfully unfollowed {len(successful)} user(s):\n" + ", ".join(successful) + "\n\n"
        if failed:
            msg += f"\u274C Failed to unfollow {len(failed)} user(s):\n" + ", ".join(failed)
        
        messagebox.showinfo("Unfollow Summary", msg)  # Display summary in a pop-up
        fetch_data()  # Refresh the data after unfollowing users
    else:
        messagebox.showinfo("No Selection", "No user selected!")  # Inform if no users are selected

    set_loading(False)  # Stop loading indicator

def toggle_select_all():
    """
    Toggles the state of all checkboxes (select or deselect all users).
    """
    value = select_all_var.get()  # Get the current state of the "Select All" checkbox
    for var in checkbox_vars:
        var.set(value and var._name)  # Set all checkbox variables to the same state

def fetch_data():
    """
    Fetches followers, following, and users not following back from GitHub.
    Initiates the data fetch in a separate thread to avoid blocking the UI.
    """
    set_loading(True)  # Show loading indicator

    def worker():
        """
        Worker function to fetch followers and following data in a background thread.
        """
        global followers_set, following_set, not_following_back
        followers = get_all(f"https://api.github.com/users/{USERNAME}/followers")  # Fetch followers
        following = get_all(f"https://api.github.com/users/{USERNAME}/following")  # Fetch following
        followers_set = set(user['login'] for user in followers)  # Set of followers' usernames
        following_set = set(user['login'] for user in following)  # Set of following usernames
        not_following_back = sorted(following_set - followers_set)  # Users not following back
        window.after(0, update_ui)  # Update the UI once data is fetched

    threading.Thread(target=worker, daemon=True).start()  # Start the worker thread

def set_loading(state):
    """
    Displays a loading message when fetching data.
    """
    loading_label.config(text="Loading..." if state else "")  # Show or hide the loading message

def update_ui():
    """
    Updates the user interface with the fetched followers, following, and users not following back data.
    """
    set_loading(False)  # Hide loading indicator

    # Clear previous stats and entries
    for label in stats_labels:
        label.destroy()
    stats_labels.clear()

    # Display follower and following statistics
    stats_labels.append(tk.Label(stats_frame, text=f"\U0001F465 Followers: {len(followers_set)}", font=("Arial", 10)))
    stats_labels.append(tk.Label(stats_frame, text=f"\u27A1\uFE0F Following: {len(following_set)}", font=("Arial", 10)))
    stats_labels.append(tk.Label(stats_frame, text=f"\u274C Not following back: {len(not_following_back)}", font=("Arial", 10)))
    for label in stats_labels:
        label.pack(anchor="w", pady=2)  # Pack the labels with some padding

    # Clear existing user entries and checkboxes
    for frame, entry, cb in entry_rows:
        frame.destroy()
    entry_rows.clear()
    checkbox_vars.clear()

    # Create new entry fields for users not following back
    for user in not_following_back:
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill="x", padx=5, pady=2)

        entry = tk.Entry(frame, width=35, relief="flat", font=("Arial", 10))
        entry.insert(0, user)  # Insert user name into the entry field
        entry.config(state="readonly")  # Make entry field read-only
        entry.pack(side="left", padx=5)

        var = tk.StringVar(name=user)  # Create variable for checkbox
        cb = tk.Checkbutton(frame, variable=var, onvalue=user, offvalue="", highlightthickness=0)  # Create checkbox
        cb.pack(side="right", padx=5)

        checkbox_vars.append(var)  # Append checkbox variable to the list
        entry_rows.append((frame, entry, cb))  # Add entry row to the list

    apply_theme()  # Apply the selected theme to the updated UI

# ------------------------------------------------------
# Create GUI Layout
# ------------------------------------------------------
window = tk.Tk()
window.title("GitHub Unfollow Tracker")  # Set window title
window.geometry("520x660")  # Set window size

is_dark_mode = True  # Default theme is dark mode
checkbox_vars, stats_labels, entry_rows = [], [], []  # Initialize lists for checkboxes, labels, and entries

# ------------------------------------------------------
# Top section with stats and buttons
# ------------------------------------------------------
stats_frame = tk.Frame(window)
stats_frame.pack(pady=5, anchor="w", padx=10)

button_frame = tk.Frame(window)
button_frame.pack(pady=(0, 10), fill="x", padx=10)

refresh_btn = tk.Button(button_frame, text="🔄 Refresh", command=fetch_data)  # Refresh button
refresh_btn.pack(side="left", padx=5)

theme_btn = tk.Button(button_frame, text="🌙 Change Theme", command=switch_theme)  # Theme switch button
theme_btn.pack(side="left", padx=5)

loading_label = tk.Label(button_frame, text="", font=("Arial", 10))  # Loading label
loading_label.pack(side="right")

# ------------------------------------------------------
# Scrollable user list section
# ------------------------------------------------------
container = tk.Frame(window)
container.pack(fill="both", expand=True, padx=10, pady=(5, 10))

canvas = tk.Canvas(container, highlightthickness=0)  # Canvas for scrollable area
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)  # Vertical scrollbar
scrollable_frame = tk.Frame(canvas)  # Frame to hold the list of users

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))  # Update scroll region
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")  # Create window within canvas
canvas.configure(yscrollcommand=scrollbar.set)  # Connect scrollbar to canvas

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ------------------------------------------------------
# Select All checkbox
# ------------------------------------------------------
select_all_var = tk.BooleanVar()  # Variable to track the state of "Select All"
select_all_cb = tk.Checkbutton(scrollable_frame, text="Select All", variable=select_all_var, command=toggle_select_all)  # Checkbox to select all
select_all_cb.pack(anchor="w", pady=(5, 5), padx=5)

# ------------------------------------------------------
# Action button to unfollow selected users
# ------------------------------------------------------
submit_btn = tk.Button(window, text="Unfollow Selections", command=show_selected, padx=10, pady=5)  # Unfollow button
submit_btn.pack(pady=(5, 10))

# ------------------------------------------------------
# Initial data load and theme application
# ------------------------------------------------------
fetch_data()  # Fetch initial data
apply_theme()  # Apply the selected theme

# Start the GUI main loop
window.mainloop()
