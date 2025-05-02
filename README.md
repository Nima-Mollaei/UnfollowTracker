

# GitHub Unfollow Tracker

This Python application helps you see who you are following on GitHub, who follows you back, and who you are following but they don't follow you back. It uses GitHub's API to fetch followers and following data and displays the results in a simple graphical user interface (GUI) built with Tkinter.

> ⏳ **Note:** It may take about **3 minutes** to start the program after launching, depending on the number of users you follow and your followers. PLEASE BE PATIENT!

---

## Features

- See how many people are following you.
- See how many people you are following.
- View the list of users you are following but they are not following you back.
- Select users and unfollow them directly from the GUI.
- Theme switch between light and dark mode.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.x**
- **Tkinter** (it should already be included with Python, but if not, you can install it separately)
- **requests** Python library

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/unfollow-tracker.git
cd unfollow-tracker
```

### 2. Install Dependencies

Use `pip` to install the required Python libraries:

```bash
pip install requests
```

> If you're on Ubuntu or Debian and Tkinter isn't installed, you can install it with:

```bash
sudo apt-get install python3-tk
```

### 3. Get Your GitHub Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens).
2. Click **Generate new token**.
3. Give it a descriptive name and select the necessary permissions (the default scope should work).
4. Copy the generated token and store it in a safe place.

### 4. Configure the Application

Open the `UnfollowTracker.py` file and update the following lines with your GitHub token and username:

```python
GITHUB_TOKEN = "your-github-token-here"
USERNAME = "your-username-here"
```

### 5. Run the Application

To start the application, simply run the script:

```bash
python UnfollowTracker.py
```

This will open a GUI window showing the number of followers, following, and the list of users you follow but who don't follow you back.

---

## How it Works

- The app uses GitHub's API to fetch the list of followers and following.
- It compares the two lists and displays users you are following but who don't follow you back.
- You can select and unfollow multiple users directly from the GUI.
- All unfollow operations are performed via GitHub's API.

---

## Example Output

```
👥 Followers: 200
➡️ Following: 500
❌ Not following back: 300
```

A list of users will appear, each with a checkbox to select and unfollow.

---

## Dark Mode Support

You can switch between light and dark modes by clicking the 🌙 **"Change Theme"** button. The list panel is slightly lighter than the background to improve visibility.

---

## Contributing

Feel free to contribute to this project! Fork the repository and submit a pull request. If you find any issues or have suggestions, please open an issue.

