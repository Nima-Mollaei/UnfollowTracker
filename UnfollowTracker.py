import tkinter as tk
import requests

# GitHub Personal Access Token and username
GITHUB_TOKEN = "your-github-token-here"
USERNAME = "your-username-here"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def get_all(url):
    results = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        results += response.json()
        url = response.links.get('next', {}).get('url')
    return results

# Get followers and following lists
followers = get_all(f"https://api.github.com/users/{USERNAME}/followers")
following = get_all(f"https://api.github.com/users/{USERNAME}/following")

followers_set = set(user['login'] for user in followers)
following_set = set(user['login'] for user in following)

# Users you follow but they don't follow you back
not_following_back = following_set - followers_set

# Create a simple Tkinter window
window = tk.Tk()
window.title("GitHub Follow Status")
window.geometry("400x400")

# Create labels to display results
label_followers = tk.Label(window, text=f"Followers: {len(followers_set)}")
label_following = tk.Label(window, text=f"Following: {len(following_set)}")
label_not_following_back = tk.Label(window, text=f"Not following back: {len(not_following_back)}")

# Display the labels on the window
label_followers.pack(pady=5)
label_following.pack(pady=5)
label_not_following_back.pack(pady=5)

# Create a Text widget to display the list of users not following back
text_box = tk.Text(window, height=10, width=40)
text_box.pack(pady=10)

# Insert the list of users not following back into the Text widget
for user in not_following_back:
    text_box.insert(tk.END, f"- {user}\n")

# Run the Tkinter main loop
window.mainloop()
