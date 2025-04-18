import tkinter as tk
from tkinter import messagebox
import requests

# ------------------------------------------------------
# GitHub credentials (Replace with your own credentials)
# ------------------------------------------------------
GITHUB_TOKEN = "your-github-token-here"
USERNAME = "your-username-here"

# Authorization headers for GitHub API
headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# ------------------------------------------------------
# Helper function to retrieve paginated data from GitHub
# ------------------------------------------------------
def get_all(url):
    results = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results += response.json()
        url = response.links.get('next', {}).get('url')
    return results

# ------------------------------------------------------
# Unfollow a specific GitHub user
# ------------------------------------------------------
def unfollow_user(user):
    url = f"https://api.github.com/user/following/{user}"
    response = requests.delete(url, headers=headers)
    return response.status_code == 204

# ------------------------------------------------------
# Handle selected checkboxes and unfollow users
# ------------------------------------------------------
def show_selected():
    selected = [var.get() for var in checkbox_vars if var.get()]
    if selected:
        successful = []
        failed = []

        for user in selected:
            if unfollow_user(user):
                successful.append(user)
            else:
                failed.append(user)

        # Create a summary message
        msg = ""
        if successful:
            msg += f"✅ Successfully unfollowed {len(successful)} user(s):\n" + ", ".join(successful) + "\n\n"
        if failed:
            msg += f"❌ Failed to unfollow {len(failed)} user(s):\n" + ", ".join(failed)

        messagebox.showinfo("Unfollow Summary", msg)
    else:
        messagebox.showinfo("No Selection", "No user selected!")

# ------------------------------------------------------
# Toggle between dark and light themes
# ------------------------------------------------------
def switch_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

# ------------------------------------------------------
# Apply selected theme to all GUI elements
# ------------------------------------------------------
def apply_theme():
    bg = "#2b2b2b" if is_dark_mode else "#ffffff"
    fg = "white" if is_dark_mode else "black"
    box_bg = "#3c3f41" if is_dark_mode else "#f0f0f0"
    box_fg = "#add8e6" if is_dark_mode else "black"

    window.configure(bg=bg)
    for label in stats_labels:
        label.config(bg=bg, fg=fg)

    container.config(bg=bg)
    canvas.config(bg=box_bg)
    scrollable_frame.config(bg=box_bg)

    for frame, entry, cb in entry_rows:
        frame.config(bg=box_bg)
        entry.config(readonlybackground=box_bg, fg=box_fg)
        cb.config(bg=box_bg, activebackground=box_bg)

    submit_btn.config(bg="#4caf50", fg="white", activebackground="#45a049")
    theme_btn.config(bg="#555555" if is_dark_mode else "#dddddd", fg="white" if is_dark_mode else "black")

# ------------------------------------------------------
# GitHub API calls to fetch followers and following users
# ------------------------------------------------------
followers = get_all(f"https://api.github.com/users/{USERNAME}/followers")
following = get_all(f"https://api.github.com/users/{USERNAME}/following")

followers_set = set(user['login'] for user in followers)
following_set = set(user['login'] for user in following)
not_following_back = sorted(following_set - followers_set)

# ------------------------------------------------------
# Create the main GUI window
# ------------------------------------------------------
window = tk.Tk()
window.title("GitHub Unfollow Tracker")
window.geometry("500x640")

is_dark_mode = True
stats_labels = []
entry_rows = []

# ------------------------------------------------------
# Show GitHub stats at the top of the window
# ------------------------------------------------------
def styled_label(text):
    label = tk.Label(window, text=text, font=("Arial", 10))
    label.pack(pady=(8, 2))
    stats_labels.append(label)
    return label

styled_label(f"👥 Followers: {len(followers_set)}")
styled_label(f"➡️ Following: {len(following_set)}")
styled_label(f"❌ Not following back: {len(not_following_back)}")

# ------------------------------------------------------
# Create a scrollable area for unfollow list
# ------------------------------------------------------
container = tk.Frame(window)
container.pack(fill="both", expand=True, padx=10, pady=(5, 10))

canvas = tk.Canvas(container, highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ------------------------------------------------------
# Display each user with a checkbox and readonly entry
# ------------------------------------------------------
checkbox_vars = []

for user in not_following_back:
    frame = tk.Frame(scrollable_frame)
    frame.pack(fill="x", padx=5, pady=2)

    entry = tk.Entry(frame, width=35, relief="flat", font=("Arial", 10))
    entry.insert(0, user)
    entry.config(state="readonly")
    entry.pack(side="left", padx=5)

    var = tk.StringVar()
    cb = tk.Checkbutton(frame, variable=var, onvalue=user, offvalue="", highlightthickness=0)
    cb.pack(side="right", padx=5)

    checkbox_vars.append(var)
    entry_rows.append((frame, entry, cb))

# ------------------------------------------------------
# Add action buttons
# ------------------------------------------------------
submit_btn = tk.Button(window, text="Unfollow Selections", command=show_selected, padx=10, pady=5)
submit_btn.pack(pady=(5, 10))

theme_btn = tk.Button(window, text="🌙 Change Theme", command=switch_theme)
theme_btn.pack(pady=(0, 10))

# Apply theme on load
apply_theme()

# ------------------------------------------------------
# Start the Tkinter event loop
# ------------------------------------------------------
window.mainloop()
