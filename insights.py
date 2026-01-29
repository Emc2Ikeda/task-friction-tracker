# Module for AI insight on task friction
from database import show_task_logs_for_task, parse_datetime
import datetime

########################################################
### Non-AI Functions ###################################
########################################################
# Summarize task completion rate & average delay based on historical data.
def get_task_summary(task_id):
    pass

# Helper function to fetch task logs
def __get_task_logs(task_id):
    # Show task logs for the selected task
    task_logs = show_task_logs_for_task(task_id)
    return task_logs

# Calculate completion rate
def get_completion_rate(task_id):
    task_logs = __get_task_logs(task_id)
    total_logs = len(task_logs)
    completed_logs_sum = sum(1 for log in task_logs if log[4])
    completion_rate = (completed_logs_sum / total_logs * 100) if total_logs > 0 else 0
    return completion_rate

# Calculate average delay in minutes
def get_average_delay(task_id):
    task_logs = __get_task_logs(task_id)
    completed_task_logs = [log for log in task_logs if log[4]]
    if completed_task_logs:
        total_delay = 0
        for log in completed_task_logs:
            planned_time = parse_datetime(log[2])
            actual_time = parse_datetime(log[3])
            if planned_time and actual_time:
                delay = (actual_time - planned_time).total_seconds()
                total_delay += delay
        average_delay_seconds = total_delay / len(completed_task_logs)
        average_delay_minutes = average_delay_seconds / 60
        return average_delay_minutes
    else:
        return None

########################################################
### AI Functions #######################################
########################################################

# Predict whether the planned task is likely to be completed on time
