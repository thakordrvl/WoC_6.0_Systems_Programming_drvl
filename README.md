# .drvl Version Control System

## Overview

`.drvl` is a command-line version control system (VCS) designed to efficiently manage file changes within a specified directory. It offers a simple and intuitive interface for users to track modifications, commit changes, and manage user settings. The tool is particularly useful for developers and anyone working with file versions in a terminal environment.

## Features

- **Easy Initialization**: Quickly set up the version control system in your desired directory.
- **File Tracking**: Add, commit, and manage files effortlessly.
- **User Management**: Set and display the username associated with your commits.
- **Comprehensive Logging**: Access and view the history of your commits.
- **Error Handling**: Robust checks to guide users through correct command usage.
- **Cross-Platform Compatibility**: Runs on Windows, macOS, and Linux.

## Installation

To get started with `.drvl`, follow these simple steps:

1. **Download the `.exe` file** from the repository. This file contains the complete version control system.
2. **Run the executable** by double-clicking on it. There’s no need to install additional dependencies or scripts.

Once the application is launched, you will be prompted to specify a directory for your version control operations.

## Usage

### Initial Setup

Upon launching `.drvl`, you will need to enter the path of the directory where you wish to initialize the version control system. This will create the necessary folder structure for tracking changes.

### Key Commands

Here are some of the primary commands available in `.drvl`:

| Command                   | Description                                         |
|---------------------------|-----------------------------------------------------|
| `help`                    | Displays a list of available commands.              |
| `location`                | Shows the current directory for the `.drvl` system. |
| `init`                    | Initializes the version control system in the specified directory. |
| `status`                  | Displays the current status of tracked files.       |
| `add <file>`              | Adds a specified file to the tracking system.       |
| `commit -m "<message>"`   | Commits the staged changes with a descriptive message. |
| `rmcommit`                | Removes the last commit from the history.           |
| `rmadd`                   | Removes all files from the staging area.            |
| `push "<dest>"`           | Pushes committed changes to the specified destination. |
| `user show`               | Displays the current username set in the system.    |
| `user set <name>`         | Sets the username for future commits.               |
| `log`                     | Displays the commit history and details.            |
| `clear`                   | Clears the terminal screen.                         |
| `checkout <hash>`         | Reverts the repository to a specific commit using its hash. |
