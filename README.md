# Game Related: Stage Management System

## Overview

This project is a Python-based stage management system designed for organizing and tracking progress through different stages of a story or project. Each stage can have dependencies, meaning that some stages need to be completed before others can be unlocked. The program allows users to mark stages as completed and view available stages based on their current progress.

## Features

- **Stage Catalog**: A list of stages with unique identifiers and dependencies.
- **Requirements Checking**: Ensures that a stage can only be completed if all its required stages have been completed.
- **User Interaction**: A command-line interface for selecting and marking stages as completed.
- **Progress Tracking**: Displays completed stages and available stages for the user.

## How It Works

1. Each stage has a unique ID, a name, and a list of required stages (dependencies).
2. The `AreRequirementsMet` method checks if all required stages have been completed before allowing a stage to be marked as complete.
3. Users can select stages from a list of available stages, mark them as completed, and track their progress.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/BynJerL/Game-Related
    ```

2. Navigate to the project directory:
    ```bash
    cd Game-Related
    ```

3. Run the Python script:
    ```bash
    python ScenesTest.py
    ```

## Usage

- Run the script to see a list of available stages.
- Select a stage by entering its number.
- The program will check if the stage's requirements are met and mark it as completed if valid.
- View your completed stages and continue until there are no more available stages.

## Code Structure

- **Stage class**: Represents a stage with an ID, name, and list of required stages.
- **`show_available_stages` function**: Returns a list of stages that can be completed based on the completed stages.
- **Main loop**: Provides an interface for the user to select and mark stages as completed.

## Example

```python
# Sample output when running the script:
Available stages:
1 <- Prologue
2 <- Act I
3 <- Act II
...

Select a stage to complete (or 0 to exit): 2
Stage 'Act I' marked as completed.
