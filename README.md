
# GitHub Follow Status App

This Python application allows you to check who you are following on GitHub, who follows you back, and who you are following but they don't follow you back. It uses GitHub's API to fetch followers and following data and displays the results in a simple graphical user interface (GUI) built with Tkinter.

## Features:
- See how many people are following you.
- See how many people you are following.
- List users you are following but they are not following you back.

## Prerequisites:
Before running this application, make sure you have the following:
- Python 3.x installed on your machine.
- A GitHub personal access token (PAT) to authenticate API requests.
- Tkinter installed (it usually comes with Python, but if not, you can install it separately).

## Setup and Installation:

### 1. Clone the repository:
First, clone this repository to your local machine.



### 2. Install dependencies:
Make sure to install the required Python libraries. You can use `pip` to install the necessary packages.

```bash
pip install requests
```

**Note:** Tkinter should already be installed with Python. If it's not, you can install it as well (for example, on Ubuntu, you can run `sudo apt-get install python3-tk`).

### 3. Get your GitHub Personal Access Token:
You will need a GitHub personal access token to authenticate with the GitHub API. To generate one:
1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens).
2. Click **Generate new token**, give it a descriptive name, and select the necessary permissions (the default scope should work).
3. Copy the generated token and keep it in a safe place.

### 4. Configure the app:
- Open the `UnfollowTracker.py` file in a text editor.
- Replace the `GITHUB_TOKEN` variable with your GitHub personal access token.
- Replace the `USERNAME` variable with your GitHub username.

```python
GITHUB_TOKEN = "your-github-token-here"
USERNAME = "your-username-here"
```

### 5. Run the app:
To start the application, simply run the Python script:


This will open a GUI window displaying the number of followers, following, and the list of users who you follow but they don't follow you back.

## How it works:
- The app uses GitHub's API to fetch the list of followers and people you are following.
- It compares the lists and shows which users you are following but who are not following you back.
- The results are displayed in a Tkinter window for easy viewing.

## Example Output:
- **Followers:** 200
- **Following:** 500
- **Not following back:** 300
- **List of users not following back:**
    - user1
    - user2
    - user3

## Contributing:
Feel free to contribute to this project by forking the repository and submitting a pull request. If you have any suggestions or encounter any issues, please open an issue.

