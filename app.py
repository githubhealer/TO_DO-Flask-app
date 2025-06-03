import json
from flask import Flask, request, redirect, url_for, render_template
from datetime import datetime, time, timedelta
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

TASKS_FILE = 'task.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def index():
    tasks_by_date = load_tasks()
    return render_template('index.html', tasks_by_date=tasks_by_date, now=datetime.now)

@app.route('/day/<date>')
def day_view(date):
    tasks_by_date = load_tasks()
    slot_minutes = int(request.args.get('slot', 30))
    slots = []
    start = datetime.strptime(date + " 04:00", "%Y-%m-%d %H:%M")
    end = datetime.strptime(date + " 20:00", "%Y-%m-%d %H:%M")
    while start < end:
        slot_end = start + timedelta(minutes=slot_minutes)
        slots.append({'start': start.strftime("%H:%M"), 'end': slot_end.strftime("%H:%M")})
        start = slot_end
    tasks = tasks_by_date.get(date, [])
    return render_template('day.html', date=date, slots=slots, tasks=tasks, slot_minutes=slot_minutes)

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

if __name__ == '__main__':
    app.run(debug=True)