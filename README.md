# TO_DO Flask App

A simple, modern, and interactive daily timetable and to-do manager built with Flask and Bootstrap.  
Features include daily task scheduling, Pomodoro timer, drag-and-drop task rescheduling, daily comments, and more.

---

## Features

- **Daily Task Scheduling:**  
  Add, edit, complete, and delete tasks for each day, organized by time slots.

- **Drag-and-Drop Task Moving:**  
  Move tasks between time slots by dragging and dropping.

- **Pomodoro Timer:**  
  Built-in Pomodoro timer with customizable work/break durations and notifications.

- **Daily Comments:**  
  Add a comment or note for each day.

- **Responsive Design:**  
  Works well on desktop and mobile.

- **Persistent Storage:**  
  Tasks and comments are stored in a JSON file (`task.json`).

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TO_DO-Flask-app.git
cd TO_DO-Flask-app
```

### 2. Install Dependencies

```bash
pip install flask
```

### 3. Run the App

```bash
python app.py
```

Or, if you have a `.bat` file for Windows:

```bash
start.bat
```

### 4. Open in Browser

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## File Structure

```
TO_DO-Flask-app/
│
├── app.py                # Main Flask application
├── task.json             # Task and comment data storage
├── templates/
│   ├── index.html        # Main agenda/month view
│   └── day.html          # Day view with tasks and comments
└── static/               # (Optional) Static files (CSS, JS, images)
```

---

## Usage

- **Add Task:**  
  Select a time slot, enter a task, and click "Add Task".

- **Edit/Delete/Complete Task:**  
  Use the buttons next to each task.

- **Move Task:**  
  Drag a task and drop it into another time slot.

- **Pomodoro Timer:**  
  Set work/break durations and use the timer for productivity.

- **Daily Comments:**  
  Add a note for each day (editable only for today).

---

## Customization

- **Time Slots:**  
  Edit the slot generation logic in `app.py` if you want different intervals.

- **Styling:**  
  Modify the CSS in the `<style>` sections of the HTML templates.

- **Notifications:**  
  The Pomodoro timer and task reminders use browser notifications (requires permission).

---

## License

MIT License

---

## Credits

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [FullCalendar](https://fullcalendar.io/) (if used)
