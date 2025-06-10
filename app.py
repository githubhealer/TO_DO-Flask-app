import json
from flask import Flask, request, redirect, url_for, render_template, jsonify
from datetime import datetime, time, timedelta
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

TASKS_FILE = 'task.json'
DAILY_COMMENTS_FILE = 'daily_comments.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

def load_daily_comments():
    if os.path.exists(DAILY_COMMENTS_FILE):
        with open(DAILY_COMMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_daily_comments(comments):
    with open(DAILY_COMMENTS_FILE, 'w') as f:
        json.dump(comments, f)

@app.route('/')
def index():
    tasks_by_date = load_tasks()
    daily_comments = load_daily_comments()
    return render_template(
        'index.html',
        tasks_by_date=tasks_by_date,
        daily_comments=daily_comments,
        now=datetime.now
    )

@app.route('/day/<date>')
def day_view(date):
    tasks_by_date = load_tasks()
    daily_comments = load_daily_comments()
    slot_minutes = int(request.args.get('slot', 30))
    slots = []
    start = datetime.strptime(date + " 04:00", "%Y-%m-%d %H:%M")
    end = datetime.strptime(date + " 20:00", "%Y-%m-%d %H:%M")
    while start < end:
        slot_end = start + timedelta(minutes=slot_minutes)
        slots.append({'start': start.strftime("%H:%M"), 'end': slot_end.strftime("%H:%M")})
        start = slot_end
    tasks = tasks_by_date.get(date, [])
    # Build a mapping from (time_slot, task.text) to index
    task_indices = {}
    for idx, task in enumerate(tasks):
        task_indices[(task['time_slot'], task['text'])] = idx
    return render_template(
        'day.html',
        date=date,
        slots=slots,
        tasks=tasks,
        slot_minutes=slot_minutes,
        task_indices=task_indices,
        daily_comments=daily_comments,
        now=datetime.now  # <-- add this
    )

@app.route('/add_task', methods=['POST'])
def add_task():
    date = request.form.get('date')
    time_slot = request.form.get('time_slot')
    title = request.form.get('title')
    tasks_by_date = load_tasks()
    if date and title and time_slot:
        tasks_by_date.setdefault(date, []).append({'text': title, 'completed': False, 'time_slot': time_slot})
        save_tasks(tasks_by_date)
    return redirect(url_for('day_view', date=date))

@app.route('/complete_task/<date>/<int:task_id>')
def complete_task(date, task_id):
    tasks_by_date = load_tasks()
    tasks = tasks_by_date.get(date, [])
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
        save_tasks(tasks_by_date)
    return redirect(url_for('day_view', date=date))

@app.route('/undo_complete_task/<date>/<int:task_id>', methods=['POST'])
def undo_complete_task(date, task_id):
    # Load tasks from your storage (e.g., task.json)
    with open('task.json', 'r') as f:
        tasks = json.load(f)
    if date in tasks and 0 <= task_id < len(tasks[date]):
        tasks[date][task_id]['completed'] = False
        with open('task.json', 'w') as f:
            json.dump(tasks, f)
    return redirect(request.referrer or url_for('day_view', date=date))

@app.route('/clear_tasks/<date>', methods=['POST'])
def clear_tasks(date):
    tasks_by_date = load_tasks()
    if date in tasks_by_date:
        tasks_by_date[date] = []
        save_tasks(tasks_by_date)
    return redirect(url_for('day_view', date=date))

@app.route('/clear_all_tasks', methods=['POST'])
def clear_all_tasks():
    save_tasks({})
    return redirect(url_for('index'))

@app.route('/edit_task/<date>/<int:task_id>', methods=['POST'])
def edit_task(date, task_id):
    tasks_by_date = load_tasks()
    new_text = request.form.get('new_text')
    next_page = request.form.get('next', 'day')
    if date in tasks_by_date and 0 <= task_id < len(tasks_by_date[date]):
        tasks_by_date[date][task_id]['text'] = new_text
        save_tasks(tasks_by_date)
    if next_page == 'agenda':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('day_view', date=date))

@app.route('/delete_task/<date>/<int:task_id>', methods=['POST'])
def delete_task(date, task_id):
    tasks_by_date = load_tasks()
    tasks = tasks_by_date.get(date, [])
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks_by_date)
    next_page = request.form.get('next', 'day')
    if next_page == 'agenda':
        return redirect(url_for('index'))
    else:
        return redirect(url_for('day_view', date=date))

@app.route('/save_daily_comment/<date>', methods=['POST'])
def save_daily_comment(date):
    comment = request.form.get('daily_comment', '')
    daily_comments = load_daily_comments()
    daily_comments[date] = comment
    save_daily_comments(daily_comments)
    return redirect(url_for('day_view', date=date))

@app.route('/comments/<date>')
def comment_by_date(date):
    daily_comments = load_daily_comments()
    comment = daily_comments.get(date)
    return render_template('comment_by_date.html', date=date, comment=comment)

@app.route('/move_task', methods=['POST'])
def move_task():
    data = request.get_json()
    task_id = int(data['task_id'])  # This is the index in the day's task list
    new_time_slot = data['new_time_slot']
    date = data['date']

    # Load tasks
    with open('task.json', 'r') as f:
        tasks = json.load(f)

    # Update the time_slot for the correct task
    if date in tasks and 0 <= task_id < len(tasks[date]):
        tasks[date][task_id]['time_slot'] = new_time_slot

        # Save back to file
        with open('task.json', 'w') as f:
            json.dump(tasks, f)

        return jsonify(success=True)
    else:
        return jsonify(success=False, error="Task not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
