# Module for AI insight on task friction
from database import show_task_logs_for_task, parse_datetime
import datetime
import torch
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

########################################################
### Non-AI Functions ###################################
########################################################
# Summarize task completion rate & average delay based on historical data.
def get_task_summary(task_id):
    pass

# Helper function to classify friction level to feed to FLAN-T5. Returns either low or high friction.
def _classify_friction(completion_rate, average_delay,
                      completion_threshold=0.5,
                      delay_threshold=60):
    
    if completion_rate < completion_threshold:
        return "high"
    
    if average_delay is not None and average_delay > delay_threshold:
        return "high"

    return "low"

# Helper function to fetch task logs
def _get_task_logs(task_id):
    # Show task logs for the selected task
    task_logs = show_task_logs_for_task(task_id)
    return task_logs

# Get task name from task ID
def get_task_name(task_id):
    task_logs = _get_task_logs(task_id)
    if task_logs:
        return task_logs[0][1]  # Assuming task name is in the second column
    return "Unknown Task"

# Calculate completion rate
def get_completion_rate(task_id):
    task_logs = _get_task_logs(task_id)
    total_logs = len(task_logs)
    completed_logs_sum = sum(1 for log in task_logs if log[4])
    completion_rate = (completed_logs_sum / total_logs) if total_logs > 0 else 0
    return completion_rate

# Calculate average delay in minutes
def get_average_delay(task_id):
    task_logs = _get_task_logs(task_id)
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
""" TODO: Calculate probability of on-time completion using logistic regression, 
    then feed this to FLAN-t5 for explanation.
"""

# Helper function to load FLAN-T5. Use cache to avoid reloading on every call.
@st.cache_resource
def _load_model():  
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

# Generate prediction context to feed into FLAN-T5 model
# def _generate_prediction_context(task_id, planned_datetime):
#     prediction_context = {
#         "completion_rate": get_completion_rate(task_id),
#         "average_delay": get_average_delay(task_id) or 0,
#         "planned_time": planned_datetime.strftime("%I:%M %p")
#     }
#     return prediction_context

# Predict whether the planned task is likely to be completed on time based on 
def show_friction_classification(task_id):
    completion_rate = get_completion_rate(task_id)
    average_delay = get_average_delay(task_id) or 0
    friction_label = _classify_friction(completion_rate, average_delay)
    tokenizer, model = _load_model()
    prompt = f"""
    Task statistics:
    - Completion rate: {completion_rate*100:.1f}%
    - Average delay: {average_delay:.1f} minutes
    - Friction classification: {friction_label}

    Complete the sentence: 

    This task shows {friction_label} friction because
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    # set num_beams to 2-4 for coherent answers. Higher values lower runtime
    outputs = model.generate(**inputs, max_length=120, num_beams=4)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

