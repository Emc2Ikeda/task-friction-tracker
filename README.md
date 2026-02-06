# task-friction-tracker

# Purpose
This Streamlit app tracks planned and actual task completion times to visualize friction patterns. It calculates completion rates and average delays for each task to help the user adjust their planning accordingly. The app does NOT determine why friction happens—it focuses only on observable behavioral patterns.

# Intended audience
This app is aimed for neurodivergent users who rely on routines but experience variable energy, sensory load, and executive functioning that make rigid planners fail.

# What is Task Friction
Task friction occurs when starting or finishing a task feels disproportionately difficult, leading to delays, avoidance, or unfinished work despite motivation. The app detects this by comparing planned versus actual completion times.
  
Example: Not beginning a task for which the time cannot be estimated (such as clearing out a cupboard), assuming there will not be adequate time, and instead wasting all the available time on social media. Not starting because knowing it will be impossible to stop – or once stopped, may be impossible to start again, resulting in cupboard’s contents left stranded on the floor for an indeterminate period. (URL: https://reframingautism.org.au/autistic-inertia-stranded-in-the-moment/)

# App Features	
  - Create and store tasks that persists across sessions.
  - Log task instances by entering planned and actual completion times.
  - Views historical logs of a selected task.
  - Automatically calculates completion rate and average delay for each task.
  - Classifies the task as low or high friction based on defined thresholds.
  - Generates AI-powered explanations of task friction in accessible language

  ## AI usage
    The app uses rule-based classification using FLAN-T5 to determine whether a task shows high or low friction based on completion rate and average delay and generate short, supportive explanations of the results. Future versions may incorporate logistic regression to provide probabilistic friction predictions.

# How to Use the App
  ## Logging the Tasks
    1. To create a new task, enter the task name and click "Add Task". Existing tasks can be selected from the "Task List" dropdown.
    2. Select the task under "Task List" and enter the planned completion time (can be in the past). If the task is complete, check "completed" box and enter the actual completion time.
    3. Click "Log Completion Time".

  ## Predict Friction Level
    1. Select a task under "Task List".
    2. (Optional) Enter the planned completion time.
    3. Click "Predict Task Friction" button.  

  ## Notes
    1. Time is rounded to the nearest 5 minutes.
    2. Hours are in 24-hour format. For PM, add 12 hours to the hour (e.g., 1:00 PM → 13:00). 
    3. For completed tasks, both planned and actual completion times must be entered; otherwise the task is considered incomplete.

# Tech Stack

# Project Structure 

# Future Improvements