# task-friction-tracker
Streamlit app that tracks planned and actual task completion time to help users identify difficult transitions.

# Project MVP:	

1. Working streamlit application, ready to be shown to someone right away

2. What can be cut: extra features

3. MVP features: 
  - User can define a routine/task: Create 1+ task/routine and persists across sessions
  - User can log task instance: Intended completion time, actual completion
  - App stores and retrieves history (persistence)
  - App shows 1+ summary: Completion time, average energy per task. Text or chart. Overall summary sentence optional

# Keywords:
friction = task not completed
  
Example: Not beginning a task for which the time cannot be estimated (such as clearing out a cupboard), assuming there will not be adequate time, and instead wasting all the available time on social media. Not starting because knowing it will be impossible to stop – or once stopped, may be impossible to start again, resulting in cupboard’s contents left stranded on the floor for an indeterminate period. (URL: https://reframingautism.org.au/autistic-inertia-stranded-in-the-moment/)

# Intended audience
Neurodivergent users who rely on routines but experience variable energy, sensory load, and executive functioning that make rigid planners fail.

# Function
Lets users log routines/tasks with simple signals (completion, energy, time of day) 

# Core value
Detects patterns of friction over time (e.g., tasks succeed more at certain times or energy levels). Identify transition points that consistently fail. It does NOT identify why the friction happened.

# AI usage
Uses basic analytics/clustering and rules to personalize insights and gentle schedule suggestions. Does not use LLMs.